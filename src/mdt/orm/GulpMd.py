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

from ..GulpMd import GulpMd
from Gulp import Gulp

class Inventory(Gulp.Inventory):
    ensemble = Gulp.Inventory.d.str(name = 'ensemble', default = 'nvt')
    ensemble.label = 'Thermodynamic Ensemble'
    ensemble.validator = Gulp.Inventory.v.choice(['nve', 'nvt', 'npt'])
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

    # XXX: see Gulp.py 
    # trajectoryfile = Gulp.Inventory.d.str(name = 'trajectoryfile', default = 'gulp.his')
    # trajectoryfile.label = 'Trajectory Filename'
    # restartfile = Gulp.Inventory.d.str(name = 'restartfile', default = 'gulp.res')
    # restartfile.label = 'Restart Filename'

    dump_restart_file_interval = Gulp.Inventory.d.float(name = 'dump_restart_file_interval', default = 5.0)
    dump_restart_file_interval.label = 'Time Interval Between Writing a Restart File (ps)'
GulpMd.Inventory = Inventory
