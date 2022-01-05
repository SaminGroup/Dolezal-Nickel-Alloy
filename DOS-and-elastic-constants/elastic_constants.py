import numpy as np
import csv

def get_elastic_tensor(filename):
    '''
    Reads the elastic tensor from the OUTCAR.

    Args:
        filename : the name of the vasp OUTCAR
    Returns:
        elastic_tensor : 6x6 tensor of the elastic moduli
    '''
    f = open(filename,"r")
    lines = f.readlines()
    f.close()
    copy = False
    elastic_tensor = []
    for line in lines:
        inp = line.split()
        if inp == []:
            continue
        if len(inp) < 4 or len(inp) > 7:
            continue
        if len(inp) == 4 and inp[0] == 'TOTAL':
            copy = True
        if copy:
            if len(inp) == 7 and len(inp[0]) == 2:
                elastic_tensor.append(inp[1:])
    return np.asarray(elastic_tensor).astype(np.float)



elastic_tensor = get_elastic_tensor('OUTCAR')
Cij = elastic_tensor/10

Sij = np.linalg.inv(Cij)

Kv = ((Cij[0,0] + Cij[1,1] + Cij[2,2]) + 2 * (Cij[0,1] + Cij[1,2] + Cij[2,0])) / 9
Kr = 1/((Sij[0,0] + Sij[1,1] + Sij[2,2]) + 2 * (Sij[0,1] + Sij[1,2] + Sij[2,0]))
Gv = (4 * (Cij[0,0] + Cij[1,1] + Cij[2,2]) - 4 * (Cij[0,1] + Cij[1,2] + Cij[2,0]) + 3 * (Cij[3,3] + Cij[4,4] + Cij[5,5]))/15
Gr = 15 / (4 * (Sij[0,0] + Sij[1,1] + Sij[2,2]) - 4 * (Sij[0,1] + Sij[1,2] + Sij[2,0]) + 3 * (Sij[3,3] + Sij[4,4] + Sij[5,5]))
Kvrh = (Kv + Kr)/2
Gvrh = (Gv + Gr)/2
mu = (3 * Kvrh - 2 * Gvrh) / (6 * Kvrh + 2 * Gvrh )
data = []
data.append("Phase {}".format(1))
data.append("Voigt bulk modulus: {} GPa".format(Kv))
data.append("Reuss bulk modulus: {} GPa".format(Kr))
data.append("Voigt shear modulus: {} GPa".format(Gv))
data.append("Reuss shear modulus: {} GPa".format(Gr))
data.append("Voigt-Reuss-Hill bulk modulus: {} GPa".format(Kvrh))
data.append("Voigt-Reuss-Hill shear modulus: {} GPa".format(Gvrh))
data.append("Isotropic Poisson ratio: {}".format(mu))
np.savetxt('Phase{}'.format(1), data, delimiter=" ", fmt="%s")
