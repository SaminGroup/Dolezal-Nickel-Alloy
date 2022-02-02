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

cl_disorb = []

folder = ["Cl-Nb-1","Cl-W-1"]
counts = [1,2,3]
final = outcar("Cl",0)
for j in range(2):
    for i in range(0,3):
        initial = outcar(folder[j],i+1)

        cl_disorb.append((final + (counts[i]/2)*BE) - initial)
################################
# W-2 EVENT
################################
initial = outcar("Cl-W-2/",1)

cl_disorb.append((final + (1/2)*BE) - initial)

################################
# Rest of the Nb and W events
################################
folder = ["Cl-Nb-2", "Cl-W-3"]
counts = [1,2]
for j in range(2):
    for i in range(0,2):
        initial = outcar(folder[j],i+1)

        cl_disorb.append((final + (counts[i]/2)*BE) - initial)

initial = outcar("Cl-Nb-3",1)

cl_disorb.append((final + (1/2)*BE) - initial)

folders = ["Nb-1", "Nb-2", "Nb-3", "W-1", "W-2", "W-3"]
Nb = []
W = []
for i in range(6):
    BE = outcar(folders[i],"_"+folders[i])
    
    initial = outcar("Cl",0)
    final = outcar(folders[i],2)
    if i < 3:
        Nb.append((final + BE) - initial)
    else:
        W.append((final + BE) - initial)

nbfolders = ["NbCl", "NbCl2", "NbCl3","NbCl-2","NbCl2-2", "NbCl-3"]
wfolders = ["WCl", "WCl2", "WCl3", "WCl-2", "WCl-3", "WCl2-3"]

nb_disorb = []
for i in range(len(nbfolders)):
    initial = outcar(nbfolders[i],1)
    final = outcar(nbfolders[i],2)
    BE = outcar(nbfolders[i],"_"+nbfolders[i])
    nb_disorb.append((final + BE) - initial)

w_disorb = []
for i in range(len(wfolders)):
    initial = outcar(wfolders[i],1)
    final = outcar(wfolders[i],2)
    BE = outcar(wfolders[i],"_"+wfolders[i])
    w_disorb.append((final + BE) - initial)

print(Nb);print("\n")
print(W);print("\n Nb Desorb \n")
print(nb_disorb);print("\n W Desorb \n")
print(w_disorb);print("\n Cl Desorb \n")
print(cl_disorb);print("\n")


w = 1
#########################################
# Nb-1 attack
########################################
fig,ax = plt.subplots(figsize=(5,4))
plt.bar(0,Nb[0],width=w,edgecolor='k',color='b',label="Nb")
plt.bar(2,nb_disorb[0],width=w,edgecolor='k')
plt.bar(3,cl_disorb[0],width=w,edgecolor='k',color='g', label="Cl")
plt.bar(5,nb_disorb[1],width=w,edgecolor='k',color='b')
plt.bar(6,cl_disorb[1],width=w,edgecolor='k',color='g')
plt.bar(8,nb_disorb[2],width=w,edgecolor='k',color='b')
plt.bar(9,cl_disorb[2],width=w,edgecolor='k',color='g')

plt.legend(ncol=2)
ax.set_xticks([0,2.5,5.5,8.5])
ax.set_xticklabels(["clean","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks([2,4,6,8])
plt.ylim(0,9)
plt.xlim(-0.75,9.75)
plt.savefig("Nb-1-desorption.png",dpi=400,bbox_inches='tight')
plt.close()
#########################################
# Nb-2 attack (only up to Cl2)
########################################
fig,ax = plt.subplots(figsize=(5,4))
plt.bar(0,Nb[1],width=w,edgecolor='k',color='b',label="Nb")
plt.bar(2,nb_disorb[3],width=w,edgecolor='k',color='b')
plt.bar(3,cl_disorb[7],width=w,edgecolor='k',color='g', label="Cl")
plt.bar(5,nb_disorb[4],width=w,edgecolor='k',color='b')
plt.bar(6,cl_disorb[8],width=w,edgecolor='k',color='g')

plt.legend(ncol=2)
ax.set_xticks([0,2.5,5.5,8.5])
ax.set_xticklabels(["clean","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks([2,4,6,8])
plt.ylim(0,9)
plt.xlim(-0.75,9.75)
plt.savefig("Nb-2-desorption.png",dpi=400,bbox_inches='tight')
plt.close()
#########################################
# Nb-3 attack (only Cl)
########################################
fig,ax = plt.subplots(figsize=(5,4))
plt.bar(0,Nb[2],width=w,edgecolor='k',color='b',label="Nb")
plt.bar(2,nb_disorb[5],width=w,edgecolor='k',color='b')
plt.bar(3,cl_disorb[11],width=w,edgecolor='k',color='g', label="Cl")

plt.legend(ncol=2)
ax.set_xticks([0,2.5,5.5,8.5])
ax.set_xticklabels(["clean","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks([2,4,6,8])
plt.ylim(0,9)
plt.xlim(-0.75,9.75)
plt.savefig("Nb-3-desorption.png",dpi=400,bbox_inches='tight')
plt.close()
#########################################
# W-1 attack (up to Cl3)
########################################
fig,ax = plt.subplots(figsize=(5,4))
plt.bar(0,W[0],width=w,edgecolor='k',color='r',label="W")
plt.bar(2,w_disorb[0],width=w,edgecolor='k',color='r')
plt.bar(3,cl_disorb[3],width=w,edgecolor='k',color='g', label="Cl")
plt.bar(5,w_disorb[1],width=w,edgecolor='k',color='r')
plt.bar(6,cl_disorb[4],width=w,edgecolor='k',color='g')
plt.bar(8,w_disorb[2],width=w,edgecolor='k',color='r')
plt.bar(9,cl_disorb[5],width=w,edgecolor='k',color='g')

plt.legend(ncol=2)
ax.set_xticks([0,2.5,5.5,8.5])
ax.set_xticklabels(["clean","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks([2,4,6,8])
plt.ylim(0,9)
plt.xlim(-0.75,9.75)
plt.savefig("W-1-desorption.png",dpi=400,bbox_inches='tight')
plt.close()
#########################################
# W-2 attack (only Cl)
########################################
fig,ax = plt.subplots(figsize=(5,4))
plt.bar(0,W[1],width=w,edgecolor='k',color='r',label="W")
plt.bar(2,w_disorb[3],width=w,edgecolor='k',color='r')
plt.bar(3,cl_disorb[6],width=w,edgecolor='k',color='g', label="Cl")

plt.legend(ncol=2)
ax.set_xticks([0,2.5,5.5,8.5])
ax.set_xticklabels(["clean","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks([2,4,6,8])
plt.ylim(0,9)
plt.xlim(-0.75,9.75)
plt.savefig("W-2-desorption.png",dpi=400,bbox_inches='tight')
plt.close()
"""
cl_disorb = [Cl-Nb-1, Cl-W-1, Cl-W-2, Cl-Nb-2, Cl-W-3, Cl-Nb-3]
          = [ 0,1,2, 3,4,5, 6, 7,8, 9,10, 11]
"""
#########################################
# W-3 attack (up to Cl2)
########################################
fig,ax = plt.subplots(figsize=(5,4))
plt.bar(0,W[2],width=w,edgecolor='k',color='r',label="W")
plt.bar(2,w_disorb[4],width=w,edgecolor='k',color='r')
plt.bar(3,cl_disorb[9],width=w,edgecolor='k',color='g', label="Cl")
plt.bar(5,w_disorb[5],width=w,edgecolor='k',color='r')
plt.bar(6,cl_disorb[10],width=w,edgecolor='k',color='g')

plt.legend(ncol=2)
ax.set_xticks([0,2.5,5.5,8.5])
ax.set_xticklabels(["clean","Cl", "Cl$_2$", "Cl$_3$"])

plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks([2,4,6,8])
plt.ylim(0,9)
plt.xlim(-0.75,9.75)
plt.savefig("W-3-desorption.png",dpi=400,bbox_inches='tight')
plt.close()
