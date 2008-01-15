import sys


def getEnergies(fileName):
    f=file(fileName)
    energies=[]
    times=[]
    while True:
        line = f.readline()
        if not line: # this kicks us out when we get to the end of the file
            break
        elif '** Time :' in line:
            times.append=float((line.split())[-3])
            continue
        elif 'Total energy      (eV) =' in line:
            energies.append=float((line.split())[-2])
            continue
    f.close()
    return energies,times

import math
import numpy as np
kb= 8.617343E-5 # eV/K

files=['Ni.345.conv.gout','Ni.691.conv.gout','Ni.1036.conv.gout','Ni.1382.conv.gout']
temps=[file.split('.')[1] for file in files]
F=[]
# loop over different temperatures
for f,T in zip(files,temps):
    #extract energies from gulp outputs
    energies,times=getEnergies(f)
    #calculate Q's and F's at each temperature
    Q=np.sum(math.exp(-1/(kb*T)*energies))/len(energies)
    F.append(-kb*T*math.log(Q))
# interpolate to get F curve--should equal energy of structure at absolute 0 (do quick minimization to find out)
np

# get entropy as a function of temperature from S = (U - F )/ T 
S=(U-F)/temps









