from pycdf import *
import numpy as np

filename='Polarizations.nc'; numks=1; numAtoms=1; numDimensions=3; numModes=numAtoms*numDimensions
cdf = CDF(filename,NC.WRITE|NC.CREATE|NC.TRUNC)
cdf.automode()
cdf.title = 'Polarizations'
k = cdf.def_dim('k',numks)
modes = cdf.def_dim('modes',numAtoms*numDimensions)
atoms = cdf.def_dim('atoms',numAtoms)
dimensions = cdf.def_dim('dimensions',numDimensions)
realOrImaginary = cdf.def_dim('realOrImaginary',2)
all = cdf.def_dim('all',numks*numModes*numAtoms*numDimensions*2)
#polarizations = cdf.def_var('polarizations', NC.DOUBLE, (k,modes,atoms,dimensions,realOrImaginary))
#
#kIndex=0; modeIndex=0; vec=np.array([[[  1.22000000e-04,  -1.73000000e-04],
#  [ -7.90000000e-05,   1.11000000e-04],
#  [ -7.17000000e-04,   1.01300000e-03]]])
#
#
#
#polarizations[kIndex,modeIndex,:,:,:]=vec


polarizations = cdf.def_var('polarizations', NC.DOUBLE, (all))
polarizations[...]=0
#polarizations[...]=[[1,2,3],[4,5,6],[7,8,9]]
#print polarizations.shape()


kIndex=0; modeIndex=0; 

vec=np.array([[[1.22000000e-04,-1.73000000e-04],[-7.90000000e-05,1.11000000e-04],[-7.17000000e-04,1.01300000e-03]]])
#vec=np.array([[1.22000000e-04, -7.90000000e-05, -7.17000000e-04]])
print vec.shape
print vec.reshape(-1)
vec=vec.reshape(-1)
startIndex=0;
#polarizations[kIndex][modeIndex][:][:][:]=vec
polarizations[startIndex:len(vec)]=vec


print polarizations


