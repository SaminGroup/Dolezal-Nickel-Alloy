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

BE_cl2 = np.loadtxt("binding_energy.txt")[0]
BE = -0.29461778
###########################
## Cl from Nb
###########################
cl_nbdesorb = []
cl2_nbdesorb = []

folder = ["NbCl", "NbCl2", "NbCl3", "NbCl4", "NbCl5"]
finalfolder = ["Cl","NbCl", "NbCl2", "NbCl3", "NbCl4"]

for j in range(len(folder)):
    initial = outcar(folder[j],0)
    final = outcar(finalfolder[j],0)
    cl_nbdesorb.append((final + BE) - initial)

    if j > 0:
        initial = outcar(folder[j],0)
        final = outcar(finalfolder[j-1],0)
        cl2_nbdesorb.append((final + BE_cl2) - initial)

###########################
## Cl from Ni
###########################
cl_nidesorb = []
cl2_nidesorb = []

folder = ["NiCl", "NiCl2", "NiCl3", "NiCl4", "NiCl5"]
finalfolder = ["Cl","NiCl", "NiCl2", "NiCl3", "NiCl4"]

for j in range(len(folder)):
    initial = outcar(folder[j],0)
    final = outcar(finalfolder[j],0)
    cl_nidesorb.append((final + BE) - initial)

    if j > 0:
        initial = outcar(folder[j],0)
        final = outcar(finalfolder[j-1],0)
        cl2_nidesorb.append((final + BE_cl2) - initial)
###########################
## Cl from W
###########################
cl_wdesorb = []
cl2_wdesorb = []

folder = ["WCl", "WCl2", "WCl3", "WCl4", "WCl5"]
finalfolder = ["Cl","WCl", "WCl2", "WCl3", "WCl4"]

for j in range(len(folder)):
    initial = outcar(folder[j],0)
    final = outcar(finalfolder[j],0)
    cl_wdesorb.append((final + BE) - initial)

    if j > 0:
        initial = outcar(folder[j],0)
        final = outcar(finalfolder[j-1],0)
        cl2_wdesorb.append((final + BE_cl2) - initial)


folders = ["Nb-1", "W-1", "Ni-1"]
Nb = []
W = []
Ni = []
for i in range(3):
    BE = outcar(folders[i],"_"+folders[i])

    initial = outcar("Cl",0)
    final = outcar(folders[i],2)
    if i == 0:
        Nb.append((final + BE) - initial)
    elif i == 1:
        W.append((final + BE) - initial)
    else:
        Ni.append((final + BE) - initial)


##-----------------------------------------------
## NbCl/WCl desorption events (Nb, NbCl, W, WCl)
##-----------------------------------------------


## NIOBIUM
nbcl_desorb = []
folder = "NbCl"
events = ["Nb", "NbCl"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nbcl_desorb.append((final + BE) - initial)

## NICKEL
nicl_desorb = []
folder = 'NiCl'
events = ["Ni", "NiCl"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nicl_desorb.append((final + BE) - initial)

## TUNGSTEN
wcl_desorb = []
folder = "WCl"
events = ["W", "WCl"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    wcl_desorb.append((final + BE) - initial)
##-----------------------------------------------
## NbCl2/WCl2 desorption events
##-----------------------------------------------

## NIOBIUM
nbcl2_desorb = []
folder = "NbCl2"
events = ["Nb", "NbCl", "NbCl2"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nbcl2_desorb.append((final + BE) - initial)

## NICKEL
nicl2_desorb = []
folder = "NiCl2"
events = ["Ni", "NiCl", "NiCl2"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nicl2_desorb.append((final + BE) - initial)

## TUNGSTEN
wcl2_desorb = []
folder = "WCl2"
events = ["W", "WCl", "WCl2"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    wcl2_desorb.append((final + BE) - initial)
##-----------------------------------------------
## NbCl3/WCl3 desorption events
##-----------------------------------------------

## NIOBIUM
nbcl3_desorb = []
folder = "NbCl3"
events = ["Nb", "NbCl", "NbCl2", "NbCl3"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nbcl3_desorb.append((final + BE) - initial)


## NICKEL
nicl3_desorb = []
folder = "NiCl3"
events = ["Ni", "NiCl", "NiCl2", "NiCl3"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nicl3_desorb.append((final + BE) - initial)


## TUNGSTEN
wcl3_desorb = []
folder = "WCl3"
events = ["W", "WCl", "WCl2", "WCl3"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    wcl3_desorb.append((final + BE) - initial)
##-----------------------------------------------
## NbCl4/WCl4 desorption events
##-----------------------------------------------

## NIOBIUM
nbcl4_desorb = []
folder = "NbCl4"
events = ["Nb", "NbCl", "NbCl2", "NbCl3", "NbCl4"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nbcl4_desorb.append((final + BE) - initial)


## NICKEL
nicl4_desorb = []
folder = "NiCl4"
events = ["Ni", "NiCl", "NiCl2", "NiCl3", "NiCl4"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nicl4_desorb.append((final + BE) - initial)


## TUNGSTEN
wcl4_desorb = []
folder = "WCl4"
events = ["W", "WCl", "WCl2", "WCl3", "WCl4"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    wcl4_desorb.append((final + BE) - initial)
##-----------------------------------------------
## NbCl5/WCl5 desorption events
##-----------------------------------------------

## NIOBIUM
nbcl5_desorb = []
folder = "NbCl5"
events = ["Nb", "NbCl", "NbCl2", "NbCl3", "NbCl4", "NbCl5"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nbcl5_desorb.append((final + BE) - initial)


## NICKEL
nicl5_desorb = []
folder = "NiCl5"
events = ["Ni", "NiCl", "NiCl2", "NiCl3", "NiCl4", "NiCl5"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    nicl5_desorb.append((final + BE) - initial)


## TUNGSTEN
wcl5_desorb = []
folder = "WCl5"
events = ["W", "WCl", "WCl2", "WCl3", "WCl4", "WCl5"]
initial = outcar(folder,0)

for i in range(len(events)):
    final = outcar(folder,i+1)
    BE = outcar(folder,"_"+events[i])
    wcl5_desorb.append((final + BE) - initial)
##-----------------------------------------------
## PLOTTING Nb
##-----------------------------------------------
nb = [nbcl_desorb,nbcl2_desorb,nbcl3_desorb, nbcl4_desorb, nbcl5_desorb]
ni = [nicl_desorb,nicl2_desorb,nicl3_desorb, nicl4_desorb, nicl5_desorb]
w = [wcl_desorb,wcl2_desorb,wcl3_desorb, wcl4_desorb, wcl5_desorb]

nb_desorb = []
nbcl_desorb = []
nbcl2_desorb = []
nbcl3_desorb = []
nbcl4_desorb = []
nbcl5_desorb = []
for i in range(len(nb)):
    nb_desorb.append(nb[i][0])
    nbcl_desorb.append(nb[i][1])
    if i > 0:
        nbcl2_desorb.append(nb[i][2])
    if i > 1:
        nbcl3_desorb.append(nb[i][3])
    if i > 2:
        nbcl4_desorb.append(nb[i][4])
    if i > 3:
        nbcl5_desorb.append(nb[i][5])

nb_desorb = np.array(nb_desorb)
nbcl_desorb = np.array(nbcl_desorb)
nbcl2_desorb = np.array(nbcl2_desorb)
nbcl3_desorb = np.array(nbcl3_desorb)
nbcl4_desorb = np.array(nbcl4_desorb)
nbcl5_desorb = np.array(nbcl5_desorb)

cl_nbdesorb = np.array(cl_nbdesorb)
cl2_nbdesorb = np.array(cl2_nbdesorb)

fig,ax = plt.subplots(figsize=(3,5))

plt.errorbar([0,1,2,3,4,5],np.concatenate((Nb,nb_desorb)),label='Nb',fmt='-s')

plt.errorbar([1,2,3,4,5],nbcl_desorb,label='NbCl', fmt='-o')

plt.errorbar([2,3,4,5],nbcl2_desorb,label='NbCl$_2$',fmt='-D')

plt.errorbar([3,4,5],nbcl3_desorb,label='NbCl$_3$',fmt='-p')

plt.errorbar([2,3,4,5],cl2_nbdesorb,label='Cl$_2$',fmt='-v')

plt.errorbar([4,5], nbcl4_desorb, label='NbCl$_4$', fmt='-X')

plt.errorbar([5], nbcl5_desorb, label='NbCl$_5$', fmt='-P',color='k')

plt.errorbar([1,2,3,4,5],cl_nbdesorb,label='Cl',fmt='-^',color='k')

plt.ylabel("E$_{des}$ (eV)")
ax.set_xticks([0,1,2,3,4,5])
ax.set_xticklabels(["0","1/15", "2/15", "3/15", "4/15", "5/15"],rotation=45)
ax.set_yticks(np.arange(1,11))
ax.set_yticks(np.arange(1.5,10.5),minor=True)
plt.ylim(0,10)
plt.xlim(-0.25,5.25)
plt.legend(ncol=2,loc='lower left')
ax.tick_params(axis='x', direction='in',top=True)
ax.tick_params(axis='y', direction='in',right=True)
ax.tick_params(axis='y', which='minor', direction='in',right=True)
plt.savefig("Nb-desorption.png",dpi=300,bbox_inches='tight')
plt.close()
##-----------------------------------------------
## PLOTTING Ni
##-----------------------------------------------
ni_desorb = []
nicl_desorb = []
nicl2_desorb = []
nicl3_desorb = []
nicl4_desorb = []
nicl5_desorb = []
for i in range(len(ni)):
    ni_desorb.append(ni[i][0])
    nicl_desorb.append(ni[i][1])
    if i > 0:
        nicl2_desorb.append(ni[i][2])
    if i > 1:
        nicl3_desorb.append(ni[i][3])
    if i > 2:
        nicl4_desorb.append(ni[i][4])
    if i > 3:
        nicl5_desorb.append(ni[i][5])


ni_desorb = np.array(ni_desorb)
nicl_desorb = np.array(nicl_desorb)
nicl2_desorb = np.array(nicl2_desorb)
nicl3_desorb = np.array(nicl3_desorb)
nicl4_desorb = np.array(nicl4_desorb)
nicl5_desorb = np.array(nicl5_desorb)

cl_nidesorb = np.array(cl_nidesorb)
cl_nidesorb[-1] = (-517.02271086 + -0.29461778) - -520.52163605
cl2_nidesorb = np.array(cl2_nidesorb)


fig,ax = plt.subplots(figsize=(3,5))

plt.errorbar([0,1,2,3,4,5],np.concatenate((Ni,ni_desorb)),label='Ni',fmt='-s')

plt.errorbar([1,2,3,4,5],nicl_desorb,label='NiCl',fmt='-o')

plt.errorbar([2,3,4,5],nicl2_desorb,label='NiCl$_2$',fmt='-D')

plt.errorbar([3,4,5],nicl3_desorb,label='NiCl$_3$',fmt='-p')

plt.errorbar([2,3,4,5],cl2_nidesorb,label='Cl$_2$',fmt='-v')

plt.errorbar([4,5],nicl4_desorb,label='NiCl$_4$',fmt='-X')

plt.errorbar([5],nicl5_desorb,label='NiCl$_5$',fmt='-P',color='k')

plt.errorbar([1,2,3,4,5],cl_nidesorb,label='Cl',fmt='-^',color='k')

plt.ylabel("E$_{des}$ (eV)")
ax.set_xticks([0,1,2,3,4,5])
ax.set_xticklabels(["0","1/15", "2/15", "3/15", "4/15", "5/15"],rotation=45)
plt.xlim(-0.25,5.25)
ax.set_yticks(np.arange(1,11))
ax.set_yticks(np.arange(1.5,10.5),minor=True)
plt.ylim(0,10)
plt.legend(ncol=2,loc='lower left')
ax.tick_params(axis='x', direction='in',top=True)
ax.tick_params(axis='y', direction='in',right=True)
ax.tick_params(axis='y', which='minor', direction='in',right=True)
plt.savefig("Ni-desorption.png",dpi=300,bbox_inches='tight')
plt.close()

fig,ax = plt.subplots(figsize=(1,1))
plt.errorbar([5],nicl5_desorb,label='NiCl$_5$',fmt='-P',color='k')
ax.set_yticks([10,11,12])
ax.set_yticks([10.5,11.5],minor=True)
plt.ylim(10,12)
ax.tick_params(axis='y', direction='in',right=True)
ax.tick_params(axis='y', which='minor', direction='in',right=True)
ax.set_xticks([3,4,5])
ax.set_xticklabels(['3/15','4/15','5/15'],rotation=45)
plt.savefig("NiCl5.png",dpi=300,bbox_inches='tight')
##-----------------------------------------------
## PLOTTING W
##-----------------------------------------------
w_desorb = []
wcl_desorb = []
wcl2_desorb = []
wcl3_desorb = []
wcl4_desorb = []
wcl5_desorb = []
for i in range(len(w)):
    w_desorb.append(w[i][0])
    wcl_desorb.append(w[i][1])
    if i > 0:
        wcl2_desorb.append(w[i][2])
    if i > 1:
        wcl3_desorb.append(w[i][3])
    if i > 2:
        wcl4_desorb.append(w[i][4])
    if i > 3:
        wcl5_desorb.append(w[i][5])

w_desorb = np.array(w_desorb)
wcl_desorb = np.array(wcl_desorb)
wcl2_desorb = np.array(wcl2_desorb)
wcl3_desorb = np.array(wcl3_desorb)
wcl4_desorb = np.array(wcl4_desorb)
wcl5_desorb = np.array(wcl5_desorb)

cl_wdesorb = np.array(cl_wdesorb)
cl_wdesorb[-1] = (-516.30015 + -0.29461778) - -520.34623202 # cl at WCl5
cl2_wdesorb = np.array(cl2_wdesorb)
cl2_wdesorb[-1] = (-512.67363 + BE_cl2) - -520.34623202


fig,ax = plt.subplots(figsize=(3,5))

plt.errorbar([0,1,2,3,4,5],np.concatenate((W,w_desorb)), label='W',fmt='-s')

plt.errorbar([1,2,3,4,5],wcl_desorb,fmt='-o',label='WCl')

plt.errorbar([2,3,4,5],wcl2_desorb,label='WCl$_2$',fmt='-D')

plt.errorbar([3,4,5],wcl3_desorb,label='WCl$_3$',fmt='-p')

plt.errorbar([2,3,4,5],cl2_wdesorb,label='Cl$_2$',fmt='-v')

plt.errorbar([4,5],wcl4_desorb,label='WCl$_4$',fmt='-X')

plt.errorbar([5],wcl5_desorb,label='WCl$_5$',fmt='-P',color='k')

plt.errorbar([1,2,3,4,5],cl_wdesorb,label='Cl',fmt='-^',color='k')



plt.ylabel("E$_{des}$ (eV)")
ax.set_yticks(np.arange(1,11))
ax.set_yticks(np.arange(1.5,10.5),minor=True)
ax.set_xticks([0,1,2,3,4,5])
ax.set_xticklabels(["0","1/15", "2/15", "3/15", "4/15", "5/15"],rotation=45)
plt.ylim(0,10)
plt.xlim(-0.25,5.25)
plt.legend(ncol=2,loc='lower left')
ax.tick_params(axis='x', direction='in',top=True)
ax.tick_params(axis='y', direction='in',right=True)
ax.tick_params(axis='y', which='minor', direction='in',right=True)
plt.savefig("W-desorption.png",dpi=300,bbox_inches='tight')
plt.close()
