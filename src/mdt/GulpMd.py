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

class GulpMd(Gulp):
    '''Gulp Md run'''
    
    ensemble = 'nvt'
    thermostat_parameter = 'None'
    barostat_parameter = 'None'
    timestep = 0.002
    equilibration_time = 0.0
    production_time = 0.0
    properties_calculation_interval = 1.0
    trajectoryfile = 'gulp.his'
    restartfile = 'gulp.res'
    dump_restart_file_interval = 1.0
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        super(GulpMd, self).__init__()
        
