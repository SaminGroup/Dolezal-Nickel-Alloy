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

folders = ["NbCl", "NbCl2", "NbCl3", "NbCl4", "NbCl5"]
nb_initial = []
nb_final = []
for afolder in folders:
    nb_initial.append(outcar(afolder,0))
    nb_final.append(outcar(afolder,1))

folders = ["NiCl", "NiCl2", "NiCl3", "NiCl4", "NiCl5"]
ni_initial = []
ni_final = []
for afolder in folders:
    ni_initial.append(outcar(afolder,0))
    ni_final.append(outcar(afolder,1))

folders = ["WCl", "WCl2", "WCl3", "WCl4", "WCl5"]
w_initial = []
w_final = []
for afolder in folders:
    w_initial.append(outcar(afolder,0))
    w_final.append(outcar(afolder,1))

nb_initial = np.array(nb_initial)
nb_final = np.array(nb_final)

ni_initial = np.array(ni_initial)
ni_final = np.array(ni_final)

w_initial = np.array(w_initial)
w_final = np.array(w_final)


Ni_bulk = -21.47862629/4
Nb_bulk = -20.42598261/2
W_bulk = -26.03210151/2

Evac_nb = (nb_initial - nb_final - Nb_bulk)
Evac_ni = (ni_initial - ni_final - Ni_bulk)
Evac_w = (w_initial - w_final - W_bulk)

Eclean_nb = [(E0 - -489.51222192 - Nb_bulk)]
Eclean_ni = [(E0 - -493.76584240 - Ni_bulk)]
Eclean_w  = [(E0 - -487.09041943 - W_bulk)]

fig,ax = plt.subplots(figsize=(4,5))

plt.errorbar([0,1,2,3,4,5],np.concatenate((Eclean_ni,Evac_ni)), label = 'Ni Attack',fmt='-s')

plt.errorbar([0,1,2,3,4,5],np.concatenate((Eclean_nb,Evac_nb)), label = 'Nb Attack',fmt='-o')

plt.errorbar([0,1,2,3,4,5],np.concatenate((Eclean_w,Evac_w)), label = 'W Attack', fmt='-D')

ax.set_xticks([0,1,2,3,4,5])
ax.set_xticklabels(["0", "1/15", "2/15", "3/15", "4/15", "5/15"],rotation=45)

ax.set_yticks([1.25,0.75,0.25,-0.25,-0.75,-1.25],minor=True)

ax.tick_params(axis='x', direction='in',top=True)
ax.tick_params(axis='y', direction='in',right=True)
ax.tick_params(axis='y', which='minor',direction='in',right=True)
plt.ylabel("Vacancy Formation Energy (eV)")
plt.xlabel("Chlorine Coverage")
plt.ylim(-1.5,1.25)
plt.legend()

plt.savefig('vacancies.png',dpi=300, bbox_inches="tight")
