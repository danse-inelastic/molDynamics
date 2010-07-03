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
from memd.gulp.Visitable import Visitable

class Optimize(Visitable):
    
    import pd
    constraints = pd.str('Constraints', default = 'None')
    constraints.meta['tip'] = '''constraints on the cell'''
    constraints.validator = pd.choice(['None', 'constant volume', 'constant pressure'])
    
    optimizeCell = pd.bool('Optimize Cell', default = False)
    optimizeCell.meta['tip'] = 'whether to optimize the unit cell'
    
    optimizeCoordinates = pd.bool('Optimize Coordinates', default = False)
    optimizeCoordinates.meta['tip'] = 'whether to optimize the coordinate positions'
    
    trajectoryFilename = pd.str('Trajectory Filename', default='molDynamics')
    trajectoryFilename.meta['tip'] = 'name of trajectory file(s)'

    restartFilename = pd.str('Restart Filename', default = 'molDynamics.res')
    restartFilename.meta['tip'] = '''restart file for resuming an md run or optimization'''
                        
    def __init__(self, name='optimize'):
        self.i=self.inventory
        self.runTypeIdentifier='optimize'
        
    def identifySettings(self, visitor): 
        return visitor.writeOptimizeSettings(self)
    
    def identifyKeywords(self, visitor): 
        return visitor.writeOptimizeKeywords(self)
    
    def identifyOptions(self, visitor): 
        return visitor.writeOptimizeOptions(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 