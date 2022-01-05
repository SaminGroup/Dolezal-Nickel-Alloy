import json
import numpy as np
import ase.io.vasp

def update_vasp_files(species, move, site, counts):

    """
    if insert is selected site is the direct coordinates of the adsorption site,
    otherwise site is the index of the adsorbate atom to be removed
    """

    names = ["Ni", "Nb", "W", "Cl", "Sb", "Te"]
    typecount = [53, 6, 13] # metal atoms
    Natoms = sum(typecount) # total number of metal atoms

    for i in range(len(counts)):
        typecount.append(counts[i]) # append adsorbate atom counts

    with open("POSCAR") as f:
        lines = f.readlines()
        f.close()

    positions = []
    count = 0
    for i in range(len(names)):
        each_type = lines[9+count:9+count+typecount[i]]
        count += typecount[i]
        positions.append(each_type)

    tempcount = counts.copy()

    if move == 0:
        tempcount[species] += 1
    else:
        tempcount[species] -= 1

    species += 3
    typecount = [53, 6, 13] # metal atoms
    for i in range(len(counts)):
        typecount.append(tempcount[i]) # append adsorbate atom counts
    #------------- remove adsorbate species with 0 atom count -----------------
    updated_names = [names[i] for i in range(len(names)) if typecount[i] != 0]
    typecount = [x for x in typecount if x != 0]
    #--------- update the POSCAR atomic name line and species count lines -----
    lines[5] = ('  '.join(updated_names)+'\n')
    lines[6] = formatter(typecount)
    #--------- add or remove the position of the selected adsorbate site ------
    if move == 0:

        positions[species].append("     {}  {}  {}  T  T  T\n".format(
                                   site[0],site[1],site[2]))
        lines = lines[:9]
        for i in range(len(positions)):
            if len(positions[i]) != 0:
                for j in range(len(positions[i])):
                    lines.append(positions[i][j])

    else:

        positions[species] = [positions[species][i] for i in range(len(positions[species])) if i != site]
        lines = lines[:9]
        for i in range(len(positions)):
            if len(positions[i]) != 0:
                for j in range(len(positions[i])):
                    lines.append(positions[i][j])


    with open("POSCAR", "w") as f:
        f.writelines(lines)
        f.close()

    potcar(updated_names)



def potcar(names):
    """
    names is a list of length m and each index is a string of the element name
    we will write to the POTCAR file in the order that is provided in the names
    list

    names = ['Type 1', 'Type 2',.., 'Type m']
    syntax of names should be captial letter followed by lowercase:

    He, Li, Au, etc
    """
    m = len(names)
    file_name = ' potcars/{}_POTCAR'

    beginning = 'cat '
    ending = ' > POTCAR'
    file_names = []
    for k in range(m):
        file_names.append(file_name.format(names[k]))
        middle = "".join(file_names)
        phrase = beginning+middle+ending

    os.system(phrase)

import os

def record_adsorption_energy(step, species, site, face):
    """
    add successive adsorption energy to model b vector and neighborhood information
    as a new row in the model A matrix
    """
    exist = os.path.exists("data/{}-ads-energy.txt".format(face))

    adsorbates = ["Cl", "Sb", "Te"]

    BE = np.array([-3.360446759999999866,-6.108018500000000017,
                   -4.444939510000000205])

    adsorbate = adsorbates[species]
    # Eads in reference to clean slab
    E0 = np.loadtxt("data/clean-electronic-energy.txt")

    # grab E1 from OUTCAR
    with open("outcars/OUTCAR{}".format(step)) as f:
        lines = f.readlines()
        f.close()
    energies = []
    for aline in lines:
        if "free  energy   TOTEN  =" in aline:
            energies.append(float(aline.split()[-2]))

    E1 = energies[-1]
    # record the successive adsorption energy
    Eads = []
    if exist:
        Eads = np.loadtxt("data/{}-ads-energy.txt".format(face))
        if Eads.shape == ():
            Eads = [Eads]
        else:
            Eads = list(Eads)


    slab = ase.io.vasp.read_vasp("poscars/POSCAR{}".format(step))

    symbols = list(slab.symbols)
    ads_present = symbols[72:]
    adscounts = []
    for i in range(3):
        count = [1 for x in ads_present if x == adsorbates[i]]
        adscounts.append(sum(count))
    adscounts = np.array(adscounts,dtype=int)

    Eads.append((E1 - E0 - sum(adscounts*(BE/2))))
    np.savetxt("data/{}-ads-energy.txt".format(face),Eads)
    neighborhood_data(step, adsorbate, face)

from numpy.linalg import norm

rcutoff = {

"100" : 3.25,
"011" : 3.85, # to cover the three corners of the adsorption triangle
"111" : 3.00

}

def neighborhood_data(step, adsorbate, face):
    """
    the newest site will be the last site listed in the slab.positions array for
    the adsorbate
    """
    slab = ase.io.vasp.read_vasp("poscars/POSCAR{}".format(step))
    a,b,c = slab.cell ; a,b = norm(a),norm(b)
    adspos = [x.position for x in slab if x.symbol == adsorbate]
    adspos = adspos[-1] # last position will be the ads site
    rc = rcutoff[face] # cutoff distance in Angstroms

    slabatoms = np.array([x.position for x in slab if norm(x.position) != norm(adspos)])
    labels = np.array([slab[i].symbol for i in range(len(slab)) if norm(slab[i].position) != norm(adspos)])

    # corner images
    corner1 = np.array([x + np.array([a,b,0]) for x in slabatoms])
    corner2 = np.array([x - np.array([a,b,0]) for x in slabatoms])
    corner3 = np.array([x + np.array([a,-b,0]) for x in slabatoms])
    corner4 = np.array([x + np.array([-a,b,0]) for x in slabatoms])
    imagea1 = np.array([x + np.array([a,0,0]) for x in slabatoms])
    imagea2 = np.array([x - np.array([a,0,0]) for x in slabatoms])
    imageb1 = np.array([x + np.array([0,b,0]) for x in slabatoms])
    imageb2 = np.array([x - np.array([0,b,0]) for x in slabatoms])

    # update potential neighbors to include images
    slabatoms = np.concatenate((slabatoms,corner1,corner2,corner3,corner4,
                                imagea1,imagea2,imageb1,imageb2))
    labels = np.concatenate((labels, labels, labels, labels, labels,
                             labels, labels, labels, labels))


    neighbors = []
    for i in range(len(slabatoms)):
        dist = np.sqrt(sum((slabatoms[i]-adspos)**2))
        if dist <= rc:
            neighbors.append(labels[i])


    symbols = ["Ni", "Nb", "W", "Cl", "Sb", "Te"]
    counts = []
    for asym in symbols:
        count = [1 for x in neighbors if x == asym]
        counts.append(sum(count))

    exist = os.path.exists("data/{}-neighborhood-matrix.txt".format(face))

    A = []
    if exist:
        with open("data/{}-neighborhood-matrix.txt".format(face)) as f:
            A = json.load(f)

    A.append(counts)
    with open("data/{}-neighborhood-matrix.txt".format(face),"w") as f:
        json.dump(A,f)

def outcar(initial):

    if initial:
        with open("OUTCAR0") as f:
            lines = f.readlines()
            f.close()
    else:
        with open("OUTCAR") as f:
            lines = f.readlines()
            f.close()

    energies = []
    for aline in lines:
        if "free  energy   TOTEN  =" in aline:
            energies.append(float(aline.split()[-2]))

    energy = energies[-1]

    if initial:
        np.savetxt("data/clean-electronic-energy.txt",[energy])

    return(energy)


def formatter(alist):
    space1 = " "
    newline = '  '.join(str(num) for num in alist)+"\n"
    return(newline)
