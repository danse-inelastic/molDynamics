#!/usr/bin/python

#import numpy
from pycdf import *


class NetcdfPolarizationWrite:
    
    def __init__(self, filename='Polarizations.nc', numks=1, numAtoms=1, numDimensions=3):
        cdf = CDF(filename,NC.WRITE|NC.CREATE|NC.TRUNC)
        cdf.automode()
        cdf.title = 'Polarizations'
        k=cdf.def_dim('k',numks)
        modes=cdf.def_dim('modes',numAtoms*numDimensions)
        atoms=cdf.def_dim('atoms',numAtoms)
        dimensions=cdf.def_dim('dimensions',numDimensions)
        realOrImaginary=cdf.def_dim('realOrImaginary',2)
        self.polarizations = cdf.def_var('polarizations', NC.DOUBLE, (k,modes,atoms,dimensions,realOrImaginary))

    def writeVec(self, kIndex, branchIndex, vec):
        """Takes numpy Polarizations with shape (N_b, D, 2) and writes to binary file."""
        #print kIndex, branchIndex, vec
        self.polarizations[kIndex][branchIndex]=vec
        print 'wrote self.polarizations[kIndex][branchIndex]=',self.polarizations[kIndex][branchIndex]


