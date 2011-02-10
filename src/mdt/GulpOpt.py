#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2007 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from mdt.Gulp import Gulp

class GulpOpt(Gulp):
    '''Gulp optimization run'''
    
    optimize_coordinates = True
    optimize_cell = False
    constraint = 'constant volume'
    trajectoryfile = 'gulp.his'
    restartfile = 'gulp.res'
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        super(GulpOpt, self).__init__()
    
try:
    class Inventory(Gulp.Inventory):
        optimize_coordinates = Gulp.Inventory.d.bool(name = 'optimize_coordinates', default = True)
        optimize_coordinates.label = 'Optimize coordinates?'
        optimize_cell = Gulp.Inventory.d.bool(name = 'optimize_cell', default = False)
        optimize_cell.label = 'Optimize the Cell'
        constraint = Gulp.Inventory.d.str(name = 'constraint', default = 'constant volume')
        constraint.label = 'constant volume'
        constraint.validator = Gulp.Inventory.v.choice(['None', 'constant volume', 'constant pressure'])
        trajectoryfile = Gulp.Inventory.d.str(name = 'trajectoryfile', default = 'gulp.his')
        trajectoryfile.label = 'Trajectory Filename'
        restartfile = Gulp.Inventory.d.str(name = 'restartfile', default = 'gulp.res')
        restartfile.label = 'Restart Filename'
    GulpOpt.Inventory = Inventory
except:
    pass
