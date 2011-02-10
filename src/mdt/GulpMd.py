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
    dump_frequency = 1.0
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        super(GulpMd, self).__init__()
    
try:
    class Inventory(Gulp.Inventory):
        ensemble = Gulp.Inventory.d.str(name = 'ensemble', default = 'nvt')
        ensemble.label = 'Thermodynamic Ensemble (nve, nvt, npt)'
        thermostat_parameter = Gulp.Inventory.d.str(name = 'thermostat_parameter', default = 'None')
        thermostat_parameter.label = 'Parameter for Thermostat'
        thermostat_parameter.help = 'only fill in if you chose the nvt or npt ensembles'
        barostat_parameter = Gulp.Inventory.d.str(name = 'barostat_parameter', default = 'None')
        barostat_parameter.label = 'Parameter for Barostat'
        barostat_parameter.help = 'only fill in if you chose the npt ensemble'
        timestep = Gulp.Inventory.d.float(name = 'timestep', default = 0.002)
        timestep.label = 'Timestep (ps)'
        equilibration_time = Gulp.Inventory.d.float(name = 'equilibration_time', default = 0.0)
        equilibration_time.label = 'Equilibration Time (ps)'
        production_time = Gulp.Inventory.d.float(name = 'production_time', default = 0.0)
        production_time.label = 'Production Time (ps)'
        
        properties_calculation_interval = Gulp.Inventory.d.float(name = 'properties_calculation_interval', default = 1.0)
        properties_calculation_interval.label = 'Time interval between material property calculation (ps)'
        trajectoryfile = Gulp.Inventory.d.str(name = 'trajectoryfile', default = 'gulp.his')
        trajectoryfile.label = 'Trajectory Filename'
        restartfile = Gulp.Inventory.d.str(name = 'restartfile', default = 'gulp.res')
        restartfile.label = 'Restart Filename'
        dump_frequency = Gulp.Inventory.d.float(name = 'dump_frequency', default = 5.0)
        dump_frequency.label = 'Time Interval Between Writing a Restart File'
    GulpMd.Inventory = Inventory
except:
    pass
