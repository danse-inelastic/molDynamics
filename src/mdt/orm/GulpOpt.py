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

    # XXX: see Gulp.py
    # trajectoryfile = Gulp.Inventory.d.str(name = 'trajectoryfile', default = 'gulp.his')
    # trajectoryfile.label = 'Trajectory Filename'
    # restartfile = Gulp.Inventory.d.str(name = 'restartfile', default = 'gulp.res')
    # restartfile.label = 'Restart Filename'


GulpOpt.Inventory = Inventory



def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['properties', 'forcefield']
    drawer.mold.sequence = [
        'optimize_coordinates',
        'optimize_cell',
        'constraint',
        'temperature', 'pressure', 
        'identify_molecules',
        'assign_bonds_from_initial_geometry',
        'calc_dispersion_in_recip_space',
        ]
    return
GulpOpt.customizeLubanObjectDrawer = customizeLubanObjectDrawer
