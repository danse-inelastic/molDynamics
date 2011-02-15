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

class Optimize(Component,Visitable):
    '''This class serves as an API/interface for md engines.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        constraints = inv.str('constraints', default = 'None')
        constraints.meta['tip'] = '''constraints on the cell'''
        constraints.validator = inv.choice(['None', 'constant volume', 'constant pressure'])
        
        optimizeCell = inv.bool('optimizeCell', default = False)
        optimizeCell.meta['tip'] = 'whether to optimize the unit cell'
        
        optimizeCoordinates = inv.bool('optimizeCoordinates', default = False)
        optimizeCoordinates.meta['tip'] = 'whether to optimize the coordinate positions'
        
        trajectoryFilename = inv.str('trajectoryFilename', default='molDynamics')
        trajectoryFilename.meta['tip'] = 'name of trajectory file(s)'

        restartFilename = inv.str('restartFilename', default = 'molDynamics.res')
        restartFilename.meta['tip'] = '''restart file for resuming an md run or optimization'''
                        
    def __init__(self, name='optimize'):
        Component.__init__(self, name, 'runType')
        self.i=self.inventory
        self.runTypeIdentifier='optimize'
        
    def identifySettings(self, visitor): 
        return visitor.writeOptimizeSettings(self)
    
    def identifyKeywords(self, visitor): 
        return visitor.writeOptimizeKeywords(self)
    
    def identifyOptions(self, visitor): 
        return visitor.writeOptimizeOptions(self)
    
#    def _configure(self):
#        Component._configure(self)
#        #self.sample = self.i.sample


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 