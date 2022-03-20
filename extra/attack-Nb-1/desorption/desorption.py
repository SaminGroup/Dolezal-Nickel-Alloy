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

BE = np.loadtxt("binding_energy.txt")[0]

DE_Cl = np.zeros((3,))

folder = "Cl/"
counts = [1,2,3]
final = outcar(folder,0)
for i in range(0,3):
    initial = outcar(folder,i+1)

    DE_Cl[i] = (final + (counts[i]/2)*BE) - initial

DE_Nb = np.zeros((4,))
DE_W = np.zeros((4,))

folders = ["Nb", "W"]
for i in range(2):
    BE = outcar(folders[i],"_"+folders[i])
    initial = outcar(folder,1)
    final = outcar(folder,2)
    if i == 0:
        DE_Nb[0] = -((final + BE) - initial)
    else:
        DE_W[0] = -((final + BE) - initial)

folders = ["NbCl", "NbCl2", "NbCl3",
           "WCl", "WCl2", "WCl3"]


for i in range(len(folders)):
    initial = outcar(folders[i],1)
    final = outcar(folders[i],2)
    BE = outcar(folders[i],"_"+folders[i])
    if i < 3:
        DE_Nb[i+1] = (final + BE) - initial
    else:
        DE_W[(i-3)+1] = (final + BE) - initial


fig,ax = plt.subplots()

x = [0.5,1,2,3]
#plt.axhline(DE[3],color = 'b', ls='--', linewidth=0.6)
#plt.axhline(DE[4],color = 'r', ls='--',linewidth=0.6)
plt.scatter(x,DE_Nb,marker='s',label="Nb")
plt.scatter(x,DE_W,marker='s',color='r',label="W")
plt.scatter(x[1:4],DE_Cl,marker='s',color='green',label="Cl")
#plt.scatter([0.5], DE[3],marker='s',color='b')
#plt.scatter([0.5], DE[4],marker='s',color='r')
plt.legend(loc="lower right")



plt.plot(x,DE_Nb,linewidth=0.75)
plt.plot(x,DE_W,linewidth=0.75,color='r')
plt.plot(x[1:4],DE_Cl,linewidth = 0.75, color='green')

ax.set_xticks([0.5,1,2,3])
ax.set_xticklabels(["--","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
plt.savefig("plot_desorption.png",dpi=400,bbox_inches='tight')
plt.close()
