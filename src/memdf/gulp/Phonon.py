#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from memdf.gulp.Visitable import Visitable

class Phonon(Visitable):
    '''This class allows phonon calculations using traditional molecular mechanics potentials.'''
    
    kpointMesh = ''
    dosAndDispersionFilename = ""
    broadenDos = False
    projectDos = ''
                        
    def __init__(self):
        self.runTypeIdentifier='phonon'
    
#    def _configure(self):
#        Component._configure(self)
#        #self.sample = self.i.sample
    
    def identifySettings( self, visitor): 
        return visitor.writePhononSettings(self)
    
    def identifyKeywords( self, visitor): 
        return visitor.writePhononKeywords(self)
    
    def identifyOptions( self, visitor): 
        return visitor.writePhononOptions(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 