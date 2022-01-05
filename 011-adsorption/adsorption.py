import os
import numpy as np
from shutil import copyfile
import adsorption_funcs as fun

def adsorption(face):
    fun.outcar(True)
    sites = np.loadtxt("{}-adsorption-sites.txt".format(face))
    sites = [sites[12],sites[5],sites[3],sites[4],sites[8],sites[10],sites[1],sites[6]]

    for i in range(len(sites)):
        with open("POSCAR{}".format(face)) as f:
            lines = f.readlines()
            f.close()

        lines.append("      {}  {}  {}  T  T  T".format(sites[i][0],sites[i][1],sites[i][2]))
        with open("POSCAR","w") as f:
            f.writelines(lines)
            f.close()

        os.system("vasp")
        copyfile("CONTCAR","poscars/POSCAR{}".format(i+1))
        copyfile("OUTCAR","outcars/OUTCAR{}".format(i+1))

        fun.record_adsorption_energy(i+1, 0, face)

adsorption("011")
