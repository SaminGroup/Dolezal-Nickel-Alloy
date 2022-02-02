import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')


trials = ["NbCl - done", "NbCl2 - done", "NbCl3"]
for trial in trials:
    with open(trial+"/spline.dat") as f:
        lines = f.readlines()
        f.close()
    data = np.zeros((len(lines),2))
    for i in range(len(data)):
        data[i] = np.asarray(lines[i].split()[1:3],dtype=float)

    plt.plot(data[:,0],data[:,1])

plt.xlabel("Reaction Coordinate")
plt.ylabel("Energy (eV)")
plt.xlim(0,max(data[:,0]))
plt.xticks(np.arange(0,max(data[:,0]),0.5))
plt.ylim(0,155)
plt.legend(["NbCl", "NbCl$_2$", "NbCl$_3$"])
plt.savefig("pathway.png",dpi=400,bbox_inches='tight')
plt.close()
