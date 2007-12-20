#!/usr/bin/python

import numpy
from struct import pack,unpack,calcsize

version=1

intSize = calcsize('<i')
dubSize = calcsize('<d')
strSize = calcsize('<s')

class PolarizationWrite:
    
    def __init__(self, filename='Polarizations', comment='',
                 dimension=3, numAtoms=1, numks=1):
        self.f=open(filename,'w')
        self.f.write(pack('<64s','Polarizations'))
        self.f.write(pack('<i',version))
        self.f.write(pack('<1024s',comment))
        self.f.write(pack('<i',dimension))
        self.f.write(pack('<i',numAtoms))
        self.f.write(pack('<i',numks))

    def writeVec(self,vec):
        """Takes numpy Polarizations with shape (N_b,D) and writes \n
to binary file."""
    
        res = numpy.zeros( vec.shape + (2,) )
        res[:,:,0] = numpy.real(vec)
        res[:,:,1] = numpy.imag(vec)
        res = tuple( res.reshape( (-1) ) )
        self.f.write( pack('<%id' % len(res),*res) )

