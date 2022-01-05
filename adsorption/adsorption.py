import os
import json
import glob
import numpy as np
from numpy import exp,log
import adsorption_funcs as fun
from random import uniform
from shutil import copyfile


def adsorption(face,newrun):
    if newrun:
        copyfile("POSCAR{}".format(face), "POSCAR0")
        # 0 - Cl, 1 - Sb, 2 - Te
        coverage = [[],[],[]]
        site_species = [[],[],[]]
        occupied = []
        counts = [0,0,0]
        energy = [fun.outcar(True),0] # generates data/clean-electron-energy.txt
        continue_step = 1

    else:
        coverage = list(np.loadtxt("data/coverage.txt").astype(int))

        infile = open('data/sites-per-species.txt')
        site_species = json.load(infile)
        infile.close()

        occupied = list(np.loadtxt("data/occupied.txt").astype(int))
        counts = np.loadtxt("data/counts.txt").astype(int)
        continue_step = len(glob.glob("poscars/POSCAR*"))+1


    copyfile("POSCAR0","POSCAR")
    sites = np.loadtxt("{}-adsorption-sites.txt".format(face))
    Nsites = len(sites)
    attempt = 0 # 0 - Cl, 1 - Sb, 2 - Te
    move = 0
    for astep in range(continue_step,Nsites+1):

        # select adsorption site
        selections = [i for i in range(len(sites)) if i not in occupied]
        r = int(uniform(0,len(selections)))
        site = sites[selections[r]]
        # update POSCAR, POTCAR files
        fun.update_vasp_files(attempt,move,site,counts)


        os.system("vasp")
        copyfile("CONTCAR","POSCAR")

        # regardless of the outcome, record the adsorption energy for the
        # adsorption for model training
        copyfile("POSCAR","poscars/POSCAR{}".format(astep))
        copyfile("OUTCAR","outcars/OUTCAR{}".format(astep))


        copyfile("POSCAR","POSCAR0") # update to new configuration

        counts[attempt] += 1
        occupied.append(selections[r])
        site_species[attempt].append(selections[r])

        for i in range(3):
            coverage[i].append(counts[i])


        np.savetxt("data/coverage.txt",coverage,fmt='%s')
        np.savetxt("data/occupied.txt",occupied,fmt='%s')
        np.savetxt("data/counts.txt",counts)
        outfile = open('data/sites-per-species.txt', "w")
        json.dump(site_species,outfile)
        outfile.close()
        fun.record_adsorption_energy(astep,attempt,site,face)
