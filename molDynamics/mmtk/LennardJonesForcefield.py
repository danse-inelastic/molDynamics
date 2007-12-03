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
from MMTK.ForceFields import LennardJonesForceField as LennardJonesFF

class LennardJonesForcefield(GeneralForcefield):
    '''Represents the Lennard Jones set of potential options from MMTK'''

    def __init__(self, name='LennardJonesForcefield'):
        Component.__init__(self, name, facility='facility')
        self.i=self.inventory

    def getForcefield(self):
        '''returns the correct mmtk forcefield object'''
        #set default values
        ljCutoff=self.i.ljCutoff
        if self.i.ljCutoff=='None (minimum image convention for periodic systems)':
            ljCutoff=None
        return LennardJonesFF(ljCutoff)
        
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
