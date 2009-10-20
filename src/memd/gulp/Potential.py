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
#from molDynamics.gulp.forcefields.ForcefieldLoader import ForcefieldLoader
from molDynamics.gulp.forcefields.InputFile import InputFile

class Potential(Component):
    '''This class serves as an API/interface for gulp potential construction.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
        dispersionInRecipSpace = inv.bool('Calculate Dispersion in Reciprocal Space', default = False)
        dispersionInRecipSpace.meta['tip'] = '''whether to calculate dispersion forces 
partly in reciprocal space'''
        useInitialBondingOnly = inv.bool('Assign Bonding Based on Initial Geometry Only', default = False)
        useInitialBondingOnly.meta['tip'] = '''instead of reassigning bonding based on every optimization or time step, use intial geometry only to
assign bonding'''
        forcefield = inv.facility('forcefield', default=InputFile('gulpLibrary'))
        forcefield.meta['tip'] = 'a class containing forcefield types'
        #forcefield.meta['known_plugins'] = ['gulpLibrary','manualEntry']
        moleculeIdentification = inv.str('Try to Identify Molecules', default = 'None')
        moleculeIdentification.meta['tip'] = '''identify molecules based on covalent radii 
and deal with intramolecular coulomb interactions'''
        moleculeIdentification.validator=inv.choice(['None','identify molecules; remove intramolecular Coulomb forces',
                                                     'identify molecules; retain intramolecular Coulomb forces'])
                        
    def __init__(self, name='potential', facility='Potential'):
        Component.__init__(self, name, facility)
        self.i=self.inventory
    
#    def _configure(self):
#        Component._configure(self)
#        #self.sample = self.i.sample

    def identifyOptions( self, visitor): 
        return visitor.writePotentialOptions(self)
    
    def identifyKeywords( self, visitor): 
        return visitor.writePotentialKeywords(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 