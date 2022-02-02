import ase.io.vasp
from ase.build import bulk

cell = bulk("W",cubic=True)

ase.io.vasp.write_vasp("POSCAR_{}".format("W"),
                           cell*(1,1,1),
                           label = '{} Cell'.format("W"),direct=True,sort=True)

print(-.50903058E+03 - -.49823466E+03 - (-20.42598261/2))


import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme()
sns.set_style('ticks')
fig,ax = plt.subplots(figsize = (8,7))
vac = [-0.316, -0.508, -0.555, -0.583]
plt.plot([1,2,3,4], vac,linewidth=0.75)
plt.scatter([1,2,3,4], vac,marker='s')
ax.set_xticks([1,2,3,4])
ax.set_xticklabels(["a","b","c","d"])
plt.ylabel("Energy of formation (eV)")
plt.savefig("vacancy.png",dpi=400,bbox_inches="tight")
