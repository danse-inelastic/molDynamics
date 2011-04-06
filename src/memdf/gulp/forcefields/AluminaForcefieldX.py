#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from memdf.gulp.forcefields.SpringGulp import SpringGulp
from memdf.gulp.forcefields.BuckinghamGulp import BuckinghamGulp  
from memdf.gulp.forcefields.ForcefieldVisitor import Visitable

class AluminaForcefieldX(Visitable):
    '''Contains the potentials for alumina
Normally this class would be created by a forcfield builder or something of that sort.    
'''
    OAndO = BuckinghamGulp('O', 'O')
    OAndAl = BuckinghamGulp('O', 'Al')
    O = SpringGulp('O')
    Al = SpringGulp('Al')

    def __init__(self):
        self.OAndO.assignInteraction('buckinghamEx1')
        self.OAndAl.assignInteraction('buckinghamEx1')
        self.O.assignInteraction('springEx1')
        self.Al.assignInteraction('springEx1')
        
    def identify(self, visitor): 
        visitor.onAluminaForcefield(self)
        self.OAndO.identify(visitor)
        self.OAndAl.identify(visitor)
        self.O.identify(visitor)
        self.Al.identify(visitor)

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Wed Jun 13 15:20:21 2007

# End of file 
