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
#from pyregui.inventory.extensions.InputFile import InputFile
from os import linesep

class InputFile(Component):
    '''On the first line input the number of atoms. On the second line input the three lattice vectors 
sequentially: x1 x2 x3 y1 y2 y3 z1 z2 z3.  On the third, fourth, etc. lines input the atoms: Zn 0.0 0.5'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        inputFile = inv.str( 'inputFile', default = "" )
#        fireballBasisSetPath = inv.str('Fireball Basis Set Path', default = None)
#        fireballBasisSetPath.meta['tip'] = 'directory containing Fdata'

    def __init__(self, name='gulpLibrary'):
        Component.__init__(self, name, facility='forcefield')
        self.i=self.inventory

    def _defaults(self):
        Component._defaults(self)

    def _configure(self):
        Component._configure(self)

    def _init(self):
        Component._init(self)
        
    def writeGulp(self):
        '''read in the file's contents and return them'''
        try:
            f=file(self.i.inputFile)
        except:
            print "cannot read forcefield file"
            raise 
        return f.read()+linesep
        


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Sun Jun 24 21:57:30 2007

# End of file 