#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                         J Brandon Keith, Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from ..GulpOpt import GulpOpt
from Gulp import Gulp

class Inventory(Gulp.Inventory):
    optimize_coordinates = Gulp.Inventory.d.bool(name = 'optimize_coordinates', default = True)
    optimize_coordinates.label = 'Optimize coordinates?'
    optimize_cell = Gulp.Inventory.d.bool(name = 'optimize_cell', default = False)
    optimize_cell.label = 'Optimize the cell?'
    constraint = Gulp.Inventory.d.str(name = 'constraint', default = 'constant volume')
    constraint.label = 'Constraint'
    constraint.validator = Gulp.Inventory.v.choice(['None', 'constant volume', 'constant pressure'])
    trajectoryfile = Gulp.Inventory.d.str(name = 'trajectoryfile', default = 'gulp.his')
    trajectoryfile.label = 'Trajectory Filename'
    restartfile = Gulp.Inventory.d.str(name = 'restartfile', default = 'gulp.res')
    restartfile.label = 'Restart Filename'
GulpOpt.Inventory = Inventory
