import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


sns.set_theme()
sns.set_style('ticks')

def outcar(folder,i):

    with open(folder+"/OUTCAR{}".format(i)) as f:
        lines = f.readlines()
        f.close()


    energies = []
    for aline in lines:
        if "free  energy   TOTEN  =" in aline:
            energies.append(float(aline.split()[-2]))

    energy = energies[-1]

    return(energy)

E0 = np.loadtxt("clean-electronic-energy.txt")
BE = np.loadtxt("binding_energy.txt")[0]

folders = ["NbCl", "NbCl2", "NbCl3", "NbCl5", "NbCl5"]
nb_energies = []
for afolder in folders:
    nb_energies.append(outcar(afolder,0))

folders = ["NiCl", "NiCl2", "NiCl3", "NiCl4", "NiCl5"]
ni_energies = []
for afolder in folders:
    ni_energies.append(outcar(afolder,0))

folders = ["WCl", "WCl2", "WCl3", "WCl4", "WCl5"]
w_energies = []
for afolder in folders:
    w_energies.append(outcar(afolder,0))

nb_energies = np.array(nb_energies)
ni_energies = np.array(ni_energies)
w_energies = np.array(w_energies)

adscounts = np.array([1,2,3,4,5])

Eads_nb = -(nb_energies - E0 - adscounts*(0.5*BE))/adscounts
Eads_ni = -(ni_energies - E0 - adscounts*(0.5*BE))/adscounts
Eads_w = -(w_energies - E0 - adscounts*(0.5*BE))/adscounts

fig,ax = plt.subplots(figsize=(4,5))

plt.axvline(3,color='g')
plt.axvline(5,color='r')

plt.errorbar([1,2,3,4,5],Eads_ni, label = 'Ni Attack',fmt='-s')

plt.errorbar([1,2,3,4,5],Eads_nb, label = 'Nb Attack',fmt='-o')

plt.errorbar([1,2,3,4,5],Eads_w, label = 'W Attack', fmt ='-D')

ax.set_xticks([1,2,3,4,5])
ax.set_xticklabels(["1/15", "2/15", "3/15", "4/15", "5/15"],rotation=45)

ax.set_yticks([2,2.5,3,3.5,4.0])
ax.set_yticks([2.25,2.75,3.25,3.75],minor=True)

ax.tick_params(axis='x', direction='in',top=True)
ax.tick_params(axis='y', direction='in',right=True)
ax.tick_params(axis='y', which='minor',direction='in',right=True)

plt.ylim(2,4)
plt.xlim(0.75,5.25)


plt.legend(loc='lower left')
plt.ylabel("Adsorption Energy (eV/Cl)")
plt.xlabel("Chlorine Coverage (ML)")

plt.savefig("adsorption-energies.png", dpi=300, bbox_inches="tight")
