import ase.io.vasp
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme()
sns.set_style('ticks')


Nsurf = 3

Ebulk = -7.36751654703125 # eV / atom ; from OUTCAR in bulk/ dir

Natoms = 72

Esurf = -500.08763645
ECl2 = -3.360446759999999866 # from Cl2 in a box, units are eV

Temps = np.array([700,800,900,1000,1100,1200])


def calc_delta_mu(Temp,PCl2):
    P = PCl2.copy()
    kT = 0.025851*(Temp/300) # units are eV
    zero_k_val = -9.181 # kJ/mol

    for i in range(len(P)):
        P[i] = 10**(P[i])
    T = np.array([700,800,900,1000,1100,1200])

    Tvals = -np.array([232.926,235.814,238.577,241.203,243.692,246.051])

    Tvals = Tvals*T / 1e3
    rel_mu0 = (Tvals - zero_k_val)
    rel_mu0 = (rel_mu0 / 96.485)/2 # eV/particle
    rel_mu0 = [rel_mu0[i] for i in range(len(T)) if T[i] == Temp][0]

    #F = np.loadtxt("helmholtz-correction")

    #F = [F[i,:] for i in range(len(T)) if T[i] == Temp][0]

    delta_mu0 = 0.5*(rel_mu0 + kT*np.log(P))
    return(delta_mu0)
    #return(delta_mu0,F)

# a dictionary for color coordinating the stability 17 colors


colors = {
3 : '#03045E',
2 : '#023E8A',
1 : '#0077B6',
0 : '#ffffff'

}


def thermo(newrun):


    EOsurf = np.array([-504.78310589,-509.37462470, -513.63052685])

    num = np.linspace(0,2,Nsurf)
    count = np.arange(1,4) + Natoms
    PCl2 = np.arange(-40,-5,1e-3)


    if newrun:
        minimum = []
        newpressure = []
        for t in range(len(Temps)):
            T = Temps[t]
            kT = 0.025851*(T/300)
            terms = np.array([0.70*np.log(0.70),0.20*np.log(0.20),0.10*np.log(0.10)])
            TS = -kT*sum(terms)

            #delta_mu0,F = calc_delta_mu(T,PCl2)
            delta_mu0 = calc_delta_mu(T,PCl2)

            mu0 = 0.5*(ECl2)
            Gibbs = np.zeros((len(PCl2),Nsurf+1))
            for i in range(len(PCl2)):
                Gibbs[i,1:] = ((EOsurf) - Esurf - (count-Natoms)*(mu0 + delta_mu0[i]) - TS) / count
                Gibbs[i,0] = -TS/Natoms

            i,j = np.where(Gibbs == np.min(Gibbs))[0][0],np.where(Gibbs == np.min(Gibbs))[1][0]

            #minimum_coverage = np.zeros((len(PCl2),2))
            minimum_coverage = np.zeros((len(PCl2),))
            for k in range(Gibbs.shape[0]):
                emin = min(Gibbs[k,:])
                for j in range(Gibbs.shape[1]):
                    if Gibbs[k,j] == emin:

                        minimum_coverage[k] = j
            # this next block of logic retains only the unique coverages and
            # pressures to avoid plotting 35,000 bars overtop one another
            CPCl2 = PCl2.copy()
            minimum_coverage, indices = np.unique(minimum_coverage,return_index=True)
            newP = np.zeros((len(indices)))
            for p in range(len(indices)):
                newP[p] = CPCl2[indices[p]]

            minimum.append(list(minimum_coverage))
            newpressure.append(list(newP))

            print("Finished scanning {} K".format(Temps[t]))
        with open("coverage.txt","w") as f:
            json.dump(minimum,f)

        with open("pressure_widths.txt","w") as f:
            json.dump(newpressure,f)


    else:
        with open("coverage.txt") as f:
            minimum = json.load(f)

        with open("pressure_widths.txt") as f:
            newpressure = json.load(f)
    # all coverages that make an appearance were first identified and the colors
    # were chosen for each
    fig,ax = plt.subplots()
    for t in range(len(Temps)):
        for p in range(len(newpressure[t])):
            c = colors[int(minimum[t][p])]
            plt.barh(Temps[t]-273.15,width = newpressure[t][p], color = c,
                     height = 100,edgecolor="none")
            """
            # fill in the remaining 2ML coverage on plot
            plt.barh(Temps[t],width = 6, color = colors[30],
                     height = 100,edgecolor="none")
            """

    plt.ylim(0,2650)
    plt.xlim(PCl2[0],-5)
    plt.ylabel("Temperature ($^{\mathrm{o}}$C)")
    plt.xlabel("$\\log_{10}(\mathrm{P}_{\mathrm{Cl_2}}/\mathrm{P^{o}})$")
    plt.xticks([-40,-35,-30,-25,-20,-15,-10,-5])
    plt.yticks(np.arange(430,980,50,dtype=int))
    #plt.legend(["Clean", "1/15 ML", "2/15 ML", "3/15 ML"],frameon=False)
    plt.ylim(430,930)
    plt.savefig('stability-graph.png',dpi=600,bbox_inches='tight')

thermo(False)
