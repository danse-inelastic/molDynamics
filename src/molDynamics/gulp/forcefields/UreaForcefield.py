#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.components.Component import Component
from molDynamics.gulp.potentials.MorseGulp import MorseGulp
from molDynamics.gulp.potentials.LennardJonesABGulp import LennardJonesABGulp
from molDynamics.gulp.potentials.ThreeBodyGulp import ThreeBodyGulp  
from molDynamics.gulp.potentials.TorsionGulp import TorsionGulp 

class UreaForcefield(Component):
    '''Contains the potentials for urea'''

    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        CAndOBond = inv.facility('C and O Bond', default=MorseGulp('C', 'O'))
        CAndNBond = inv.facility('C and N Bond', default=MorseGulp('C', 'N'))
        HAndNBond = inv.facility('H and N Bond', default=MorseGulp('H', 'N'))
        CAndO = inv.facility('C and O Potential', default=LennardJonesABGulp('C', 'O'))
        CAndN = inv.facility('C and N Potential', default=LennardJonesABGulp('C', 'N'))
        OAndO = inv.facility('O and O Potential', default=LennardJonesABGulp('O', 'O'))
        NAndO = inv.facility('N and O Potential', default=LennardJonesABGulp('N', 'O'))
        NAndN = inv.facility('N and N Potential', default=LennardJonesABGulp('N', 'N'))
        CAndC = inv.facility('C and C Potential', default=LennardJonesABGulp('C', 'C'))
        NAndCAndO = inv.facility('N, C and O Potential', default=ThreeBodyGulp('N', 'C', 'O'))
        HAndNAndC = inv.facility('H, N, and C Potential', default=ThreeBodyGulp('H', 'N', 'C'))
        HAndNAndH = inv.facility('H, N, and H Potential', default=ThreeBodyGulp('H', 'N', 'H'))
        NAndCAndN = inv.facility('N, C, and N Potential', default=ThreeBodyGulp('N', 'C', 'N'))
        OAndCAndNAndH = inv.facility('O, C, N, and H Potential', default=TorsionGulp('O', 'C', 'N', 'H'))
        NAndCAndNAndH = inv.facility('N, C, N, and H Potential', default=TorsionGulp('N', 'C', 'N', 'H'))
        OAndCAndNAndN = inv.facility('O, C, N, and N Potential', default=TorsionGulp('O', 'C', 'N', 'N'))

    def __init__(self, name=None):
        if name is None:
            name = 'Urea Forcefield'
        Component.__init__(self, name, facility='facility')
        self.i=self.inventory
        self.i.CAndOBond.assignInteraction('morseGulpEx10')
        self.i.CAndOBond.i.interIntra = 'intramolecular'
        self.i.CAndNBond.assignInteraction('morseGulpEx10')
        self.i.CAndNBond.i.interIntra = 'intramolecular'
        self.i.HAndNBond.assignInteraction('morseGulpEx10')
        self.i.HAndNBond.i.interIntra = 'intramolecular'
        self.i.CAndO.assignInteraction('lennardGulpEx10')
        self.i.CAndO.i.interIntra = 'intermolecular'
        self.i.CAndN.assignInteraction('lennardGulpEx10')
        self.i.CAndN.i.interIntra = 'intermolecular'
        self.i.OAndO.assignInteraction('lennardGulpEx10')
        self.i.OAndO.i.interIntra = 'intermolecular'
        self.i.NAndO.assignInteraction('lennardGulpEx10')
        self.i.NAndO.i.interIntra = 'intermolecular'
        self.i.NAndN.assignInteraction('lennardGulpEx10')
        self.i.NAndN.i.interIntra = 'intermolecular'
        self.i.CAndC.assignInteraction('lennardGulpEx10')  
        self.i.CAndC.i.interIntra = 'intermolecular'     
        self.i.NAndCAndO.assignInteraction('threeBodyGulpEx10')
        self.i.HAndNAndC.assignInteraction('threeBodyGulpEx10')
        self.i.HAndNAndH.assignInteraction('threeBodyGulpEx10')
        self.i.NAndCAndN.assignInteraction('threeBodyGulpEx10')
        self.i.OAndCAndNAndH.assignInteraction('torsionGulpEx10')
        self.i.NAndCAndNAndH.assignInteraction('torsionGulpEx10')
        self.i.OAndCAndNAndN.assignInteraction('torsionGulpEx10')

    def writeGulp(self):
        '''writes out all the potentials in gulp format'''
        lines=self.i.CAndOBond.write()\
        +self.i.CAndNBond.write()\
        +self.i.HAndNBond.write()\
        +self.i.CAndO.write()\
        +self.i.CAndN.write()\
        +self.i.OAndO.write()\
        +self.i.NAndO.write()\
        +self.i.NAndN.write()\
        +self.i.CAndC.write()\
        +self.i.HAndNAndC.write()\
        +self.i.HAndNAndH.write()\
        +self.i.NAndCAndN.write()\
        +self.i.OAndCAndNAndH.write()\
        +self.i.NAndCAndNAndH.write()\
        +self.i.OAndCAndNAndN.write()
        return lines
        
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
