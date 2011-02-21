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
            'trajectoryfile',
            'restartfile',
            'logfile',
            'inputfile',
            ]
        return

