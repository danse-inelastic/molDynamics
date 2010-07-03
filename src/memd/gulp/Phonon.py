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
from pyre.components.Component import Component
from memd.gulp.Visitable import Visitable

class Phonon(Component,Visitable):
    '''This class allows phonon calculations using traditional molecular mechanics potentials.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
        kpointMesh = inv.str('Monkhorst Pack mesh', default = "")
        kpointMesh.meta['tip'] = '''integer triplet representing Monkhorst Pack mesh 
for integrating the Brillouin zone (i.e. 2 4 4)'''
        
        dosAndDispersionFilename = inv.str('Filename for DOS Output', default = "")
        dosAndDispersionFilename.meta['tip'] = '''filename for DOS and/or dispersion output files'''

#        engineExecutablePath = InputFile('Engine Executable Path', default = ".")
#        engineExecutablePath.meta['tip'] = '''path to the engine's executable'''
        broadenDos = inv.bool('Broaden the DOS', default = False)
        broadenDos.meta['tip'] = '''broaden the density of states'''
        
        projectDos = inv.str('Project the DOS onto certain species', default = '')
        projectDos.meta['tip'] = '''species names separated by spaces (i.e. H Li)'''        

                        
    def __init__(self, name='phonon'):
        Component.__init__(self, name, 'runType')
        self.i=self.inventory
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