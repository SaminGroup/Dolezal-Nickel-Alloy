import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')

with open("DOSCAR") as f:
    dos = f.readlines()
    f.close()
fermi = 6.40367661
tdos = dos[5:306]
pdos = dos[306:]

dos_mat = np.zeros((len(tdos),5))
pdos_mat = np.zeros((len(pdos),19))
for i in range(len(tdos)):
    dos_mat[i] = np.asarray(tdos[i].split(),dtype=float)
for i in range(len(pdos)):
    pdos_mat[i] = np.asarray(pdos[i].split(),dtype=float)


nidos = pdos_mat[:3*301,:]
step1 = 3*301
nbdos = pdos_mat[step1+1:step1+(5*301),:]
step2 = step1+(5*301)
wdos = pdos_mat[step2+1:step2+(2*301),:]

shell = ["s", "p", "d"]
selected_shell = [[],[],[],[],[]]
#-----------------------------------------------------------------------------
# Separate PDOS into each species contribution
#-----------------------------------------------------------------------------
Nidos = np.zeros((nidos.shape[0],2))
for i in range(nidos.shape[0]):
    if nidos[i,0] >= -15:
        Nidos[i] = np.array([nidos[i,0],max(nidos[i,1:])])
        pickshell = np.where(nidos[i,1:] == np.max(nidos[i,1:]))[0][0]
        # added logic to determine which shell the dos was pulled from
        if pickshell != 0:
            if pickshell == 1:
                selected_shell[0].append(1)
            elif 1 < pickshell < 5:
                selected_shell[0].append(2)
            elif 5 <= pickshell < 13:
                selected_shell[0].append(3)


Nbdos = np.zeros((nbdos.shape[0],2))
for i in range(nbdos.shape[0]):
    if nbdos[i,0] >= -15:
        Nbdos[i] = np.array([nbdos[i,0],max(nbdos[i,1:])])
        pickshell = np.where(nbdos[i,1:] == np.max(nbdos[i,1:]))[0][0]
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[1].append(1)
            elif 4 < pickshell < 7:
                selected_shell[1].append(2)
            else:
                selected_shell[1].append(3)

Wdos = np.zeros((wdos.shape[0],2))
for i in range(wdos.shape[0]):
    if wdos[i,0] >= -15:
        Wdos[i] = np.array([wdos[i,0],max(wdos[i,1:])])
        pickshell = np.where(wdos[i,1:] == np.max(wdos[i,1:]))[0][0]
        if pickshell != 0:
            if pickshell < 4:
                selected_shell[2].append(1)
            elif 4 < pickshell < 7:
                selected_shell[2].append(2)
            else:
                selected_shell[2].append(3)


counts = [[],[],[]]
for a,b,c in zip(Nidos,Nbdos,Wdos):
    energy = [a[0],b[0],c[0]]
    count = [0,0,0]
    for a1,b1,c1 in zip(Nidos,Nbdos,Wdos):
        if a1[0] == energy[0]:
            count[0] += a1[1]
        if b1[0] == energy[1]:
            count[1] += b1[1]
        if c1[0] == energy[2]:
            count[2] += c1[1]


    counts[0].append(count[0]);counts[1].append(count[1]);counts[2].append(count[2])
#-----------------------------------------------------------------------------
# Generate histograms for the state count bar plot
#-----------------------------------------------------------------------------
nicount,nibins = np.histogram(selected_shell[0],3);nibins = nibins[:-1]
nbcount,nbbins = np.histogram(selected_shell[1],3);nbbins = nbbins[:-1]
wcount,wbins = np.histogram(selected_shell[2],3);wbins = wbins[:-1]
#-----------------------------------------------------------------------------
# Number of States bar plot
#-----------------------------------------------------------------------------
w = 0.1
fig,ax = plt.subplots()
x=np.array([1,2,3])
plt.bar(x+(1*w),nicount,width=w,edgecolor="k")
plt.bar(x-(1*w),nbcount,width=w,edgecolor="k")
plt.bar(x,wcount,width=w,edgecolor="k")

ax.set_xticks(x)
ax.set_xticklabels(shell)
plt.xlim(0.7,3.3)
plt.yticks([])
plt.ylabel("Number of States")
plt.savefig("NoS.png",dpi=400,bbox_inches="tight")
#-----------------------------------------------------------------------------
# Density of States bar plot
#-----------------------------------------------------------------------------
plt.close()
w = 0.15
fig,ax = plt.subplots()
total = [sum(x) for x in counts]
plt.bar(Nidos[:601,0]-fermi,counts[0],width=w,edgecolor="k")
plt.bar(Nbdos[:601,0]-fermi,counts[1],width=w,edgecolor="k")
plt.bar(Wdos[:601,0]-fermi,counts[2],width=w,edgecolor="k")

plt.xlabel("E-E${}_{f}$ (eV)") ; plt.ylabel("Density of States")
plt.xlim(-15,15)
#plt.legend(["Ni","Nb","W"],ncol=3,fontsize=18,frameon=False)
plt.axvline(0,color="k",ls="--")
plt.ylim(0,np.max(counts)+0.05)
plt.yticks([])
plt.savefig("DoS.png",dpi=400,bbox_inches='tight')
#-----------------------------------------------------------------------------
