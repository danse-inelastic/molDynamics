#!/usr/bin/python

#import numpy
from pycdf import *


class NetcdfPolarizationWrite:
    
    def __init__(self, filename='Polarizations.nc', numks=1, numAtoms=1, numDimensions=3):
        numModes=numAtoms*numDimensions
        cdf = CDF(filename,NC.WRITE|NC.CREATE|NC.TRUNC)
        cdf.automode()
        cdf.title = 'Polarizations'
        numksAtt = cdf.attr('numks')             
        numAtomsAtt = cdf.attr('numAtoms')   
        numDimensionsAtt = cdf.attr('numDimensions')       
        numksAtt.put(NC.INT, numks)          
        numAtomsAtt.put(NC.INT, numAtoms)      
        numDimensionsAtt.put(NC.INT, numDimensions)
        
#        k=cdf.def_dim('k',numks)
#        modes=cdf.def_dim('modes',numAtoms*numDimensions)
#        atoms=cdf.def_dim('atoms',numAtoms)
#        dimensions=cdf.def_dim('dimensions',numDimensions)
#        realOrImaginary=cdf.def_dim('realOrImaginary',2)
#        self.polarizations = cdf.def_var('polarizations', NC.DOUBLE, (k,modes,atoms,dimensions,realOrImaginary))
        
        all = cdf.def_dim('all',numks*numModes*numAtoms*numDimensions*2)
        
        self.polarizations = cdf.def_var('polarizations', NC.DOUBLE, (all))
        #self.polarizations.a
        
        self.polarizations[...]=0
        self.currentIndex=0

    def writeVec(self, vec):
        """Takes numpy Polarizations and writes to binary file."""
        #print 'vec to be written',vec
        vec=vec.reshape(-1)
        #print vec
#        self.polarizations[kIndex][branchIndex]=vec
#        print 'wrote self.polarizations[kIndex][branchIndex]=',self.polarizations[kIndex][branchIndex]
        #print 'polarizations before',self.polarizations[self.currentIndex:self.currentIndex+len(vec)]
        self.polarizations[self.currentIndex:self.currentIndex+len(vec)]=vec
        #print 'vec written',self.polarizations[self.currentIndex:self.currentIndex+len(vec)]
        self.currentIndex+=len(vec)
        


