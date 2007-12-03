#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from GeneralForcefield import GeneralForcefield
from pyre.components.Component import Component
from MMTK.ForceFields import Amber99ForceField, Amber94ForceField

class AmberForcefield(GeneralForcefield):
    '''Represents the Amber set of potential options from MMTK'''
    class Inventory(GeneralForcefield.Inventory):
        import pyre.inventory as inv
        electrostaticCutoff = inv.str('Electrostatic Cutoff (nm)', default = 'None (ewald summation for periodic systems)')
        electrostaticCutoff.meta['tip'] = 'cutoff for electrostatic interactions'
        type = inv.str('Type of Forcefield',default='Amber94')
        type.validator = inv.choice(['Amber94','Amber99'])

    def __init__(self, name='AmberForcefield'):
        Component.__init__(self, name, facility='facility')
        self.i=self.inventory

    def getForcefield(self):
        '''returns the correct mmtk forcefield object'''
        #set default values
        ljCutoff=self.i.ljCutoff
        electrostaticCutoff=self.i.electrostaticCutoff
        if self.i.ljCutoff=='None (minimum image convention for periodic systems)':
            ljCutoff=None
        if self.i.electrostaticCutoff=='None (minimum image convention for periodic systems)':
            electrostaticCutoff=None
        if self.i.type=='Amber94':
            return Amber94ForceField(ljCutoff, electrostaticCutoff)
        elif self.i.type=='Amber99':
            return Amber99ForceField(ljCutoff, electrostaticCutoff)
        

        
    def _defaults(self):
        Component._defaults(self)
        return

    def _configure(self):
        Component._configure(self)
        return

    def _init(self):
        Component._init(self)
        return


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Wed Jun 13 15:20:21 2007

# End of file 
