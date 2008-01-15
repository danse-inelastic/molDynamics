#!/usr/bin/python

#--- User setup ---------------------------------------------------
sym  = 'Ni'
temps=['0345','0691','1036','1382']
files=[temp + '/' + sym + '.conv.gout' for temp in temps]

#weird Brandon setup
#files=['Ni.345.conv.gout','Ni.691.conv.gout','Ni.1036.conv.gout','Ni.1382.conv.gout']
#temps=[file.split('.')[1] for file in files]

#--- Imports ------------------------------------------------------
import numpy as np
kb= 8.617343E-5 # eV/K

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
# loop over different temperatures
for f,T in zip(files,temps):
    T = float(T)
    #extract energies from gulp outputs
    energies,times=getEnergies(f)
    #calculate Q's and F's at each temperature
    Q=np.sum( np.exp(energies/(kb*T)) )    #/float( len(energies) )
    U.append(np.sum(np.exp(energies/(kb*T)) )/Q)     #/float( len(energies) )
    F.append(kb*T*np.log(Q))

# interpolate to get F -- should equal energy of structure at absolute 0 
#   (do quick minimization to find out)

# get entropy as a function of temperature from S = (U - F )/ T 
#   S=(U-F)/temps









