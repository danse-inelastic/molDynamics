#!/usr/bin/python

#--- User setup ---------------------------------------------------
sym  = 'Ni'
temps=['0345','0691','1036','1382']
#files=[temp + '/' + sym + '.conv.gout' for temp in temps]

#--- OR: ---
from os import sep
baseDir='/home/jbk/gulp3.0/z_py/Ni'+sep
temps=['345','691','1036','1382']
files=[ baseDir+sym + '.' + str(int(temp)) + '.conv.gout' for temp in temps]

#--- Imports ------------------------------------------------------
import numpy as np
import math
kb= 8.617343E-5 # eV/K
h = 4.1356673328075734E-15 # eV * s

#--- File parsing -------------------------------------------------
def getEnergies(fileName):
    f=file(fileName)
    energies=[]
    times=[]
    while True:
        line = f.readline()
        if not line: # kicks us out at the end of the file
            break
        elif '** Time :' in line:
            times.append( float((line.split())[-3]) )
            continue
        elif 'Total energy      (eV) =' in line:
            energies.append( float((line.split())[-2]) )
            continue
    f.close()
    return np.array(energies),np.array(times)

#--- Get the free energy ------------------------------------------

F=[]
U=[]
eVToMegaeV=1e-6
N=864
shift=3975
statMechNormalizer= -3*N*math.log(h) - (1/2.*math.log(2*math.pi*N) + N*math.log(N) - N)
# loop over different temperatures
for f,T in zip(files,temps):
    T = float(T)
    #extract energies from gulp outputs
    energies,times = getEnergies(f)
    shiftedEnergies = energies/(kb*T) + shift/(kb*T)
    boltzFactor = np.exp(shiftedEnergies)
    #calculate Q's and F's at each temperature
    Q =       np.sum( boltzFactor )    #/float( len(energies) )
    U.append( np.dot(energies, boltzFactor)/Q) #/float( len(energies) )
    F.append(-kb*T*(np.log(Q)+statMechNormalizer))

# interpolate to get F -- should equal energy of structure at absolute 0
#   (do quick minimization to find out)

# get entropy as a function of temperature from S = (U - F )/ T
#   S=(U-F)/temps








