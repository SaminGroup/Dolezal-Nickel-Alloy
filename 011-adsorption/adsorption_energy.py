import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

Ni = np.array([1, 2, 1, 1, 1, 1, 1, 1])
Nb = np.array([2, 2, 0, 0, 1, 1])
W  = np.array([0, 0, 3/2, 3/2, 1/2, 1/2])

ads_energy = -np.array([
-3.015246060000010608,
-3.067635179999997241,
-2.628014449999995783,
-2.512830050000020243,
-2.668901270000021420,
-2.965071950000010226])

fig,ax = plt.subplots()



plt.scatter(Nb,ads_energy,marker="s")
plt.scatter(W,ads_energy,marker="s",c="r")
ax.set_xticks([0,0.5,1,1.5,2])
ax.set_xticklabels(["--", "W", "Nb", "W$_2$", "Nb$_2$"])
plt.ylabel("E$_{ads}$ (eV)")
plt.savefig("adsorption-energy.png",dpi=400,bbox_inches='tight')
