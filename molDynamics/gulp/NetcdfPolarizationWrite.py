#!/usr/bin/python

import numpy
from pycdf import *


class NetcdfPolarizationWrite:
    
    def __init__(self, filename='Polarizations.nc', comment='', numDimensions=3, numAtoms=1, numks=1):
        cdf = CDF(filename,NC.WRITE|NC.CREATE)
        cdf.automode()
        cdf.title = 'Polarizations'
        k=cdf.def_dim('k',numks)
        branches=cdf.def_dim('branches',numAtoms*numDimensions)
        atoms=cdf.def_dim('atoms',numAtoms)
        dimensions=cdf.def_dim('dimensions',numDimensions)
        realOrImaginary=cdf.def_dim('realOrImaginary',2)
        self.polarizations = cdf.def_var('polarizations', NC.DOUBLE, (k,branches,atoms,dimensions,realOrImaginary))

    def writeVec(self, kIndex, vec):
        """Takes numpy Polarizations with shape (N_b, D) and writes to binary file."""
        self.polarizations[kIndex][:][:][:]=vec
        #res = numpy.zeros( vec.shape + (2,) )
        #res[:,:,0] = numpy.real(vec)
        #res[:,:,1] = numpy.imag(vec)
        #res = tuple( res.reshape( (-1) ) )
        #self.f.write( pack('<%id' % len(res),*res) )


