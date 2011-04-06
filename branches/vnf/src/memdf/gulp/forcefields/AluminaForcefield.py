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
from memdf.gulp.forcefields.SpringGulp import SpringGulp
from memdf.gulp.forcefields.BuckinghamGulp import BuckinghamGulp  

class AluminaForcefield(Component):
    '''Contains the potentials for alumina'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        OAndO = inv.facility('O-O Potential', default = BuckinghamGulp('O', 'O'))
        OAndAl = inv.facility('O-Al Potential', default = BuckinghamGulp('O', 'Al'))
        O = inv.facility('O Potential', default = SpringGulp('O'))
        Al = inv.facility('Al Potential', default = SpringGulp('Al'))

    def __init__(self, name=None):
        if name is None:
            name = 'Urea Forcefield'
        Component.__init__(self, name, facility='facility')
        self.i=self.inventory
        self.i.OAndO.assignInteraction('buckinghamEx1')
        self.i.OAndAl.assignInteraction('buckinghamEx1')
        self.i.O.assignInteraction('springEx1')
        self.i.Al.assignInteraction('springEx1')

    def writeGulp(self):
        '''writes out all the forcefields in gulp format'''
        lines=self.i.CAndOBond.write()\
        +self.i.OAndO.write()\
        +self.i.OAndAl.write()\
        +self.i.O.write()\
        +self.i.Al.write()
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
