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

class Mmtk(object):
    '''mmtk md run'''
    
    matter = None
    temperature = 300.0
    pressure = 0.0
    
    forcefield_name='amber99'
    ensemble = 'nvt'
    thermostat_parameter = 'None'
    barostat_parameter = 'None'
    timestep = 0.002
    equilibration_time = 0.0
    production_time = 0.0
    properties_calculation_interval = 1.0
    trajectoryfile = 'mmtk.nc'
    restartfile = 'mmtk.res'
    logfile = 'mmtk.log'
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
try:
    from dsaw.model.Inventory import Inventory as InvBase
    from matter.orm.Structure import Structure
    class Inventory(InvBase):
        matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
        matter.label = 'Structure' 
        temperature = InvBase.d.float(name = 'temperature', default = 300.0)
        temperature.label = 'Temperature or Initial Energy (K)' 
        pressure = InvBase.d.float(name = 'pressure', default = 0.0)
        pressure.label = 'Pressure (GPa)' 
        
        forcefield_name = InvBase.d.str(name = 'forcefield_name', default = 'None')  
        forcefield_name.label = 'Name of Forcefield'
        forcefield_name.validator = InvBase.v.choice(['amber99', 'amber94', 'lennard jones'])
        
        ensemble = InvBase.d.str(name = 'ensemble', default = 'nvt')
        ensemble.label = 'Thermodynamic Ensemble'
        ensemble.validator = InvBase.v.choice(['nve', 'nvt', 'npt'])
        thermostat_parameter = InvBase.d.str(name = 'thermostat_parameter', default = 'None')
        thermostat_parameter.label = 'Parameter for Thermostat'
        thermostat_parameter.help = 'only fill in if you chose the nvt or npt ensembles'
        barostat_parameter = InvBase.d.str(name = 'barostat_parameter', default = 'None')
        barostat_parameter.label = 'Parameter for Barostat'
        barostat_parameter.help = 'only fill in if you chose the npt ensemble'
        timestep = InvBase.d.float(name = 'timestep', default = 0.002)
        timestep.label = 'Timestep (ps)'
        equilibration_time = Invbase.d.float(name = 'equilibration_time', default = 0.0)
        equilibration_time.label = 'Equilibration Time (ps)'
        production_time = InvBase.d.float(name = 'production_time', default = 0.0)
        production_time.label = 'Production Time (ps)'
        
        properties_calculation_interval = InvBase.d.float(name = 'properties_calculation_interval', default = 1.0)
        properties_calculation_interval.label = 'Time interval between material property calculation (ps)'
        trajectoryfile = InvBase.d.str(name = 'trajectoryfile', default = 'mmtk.nc')
        trajectoryfile.label = 'Trajectory Filename'
        restartfile = InvBase.d.str(name = 'restartfile', default = 'mmtk.res')
        restartfile.label = 'Restart Filename'
        logfile = InvBase.d.str(name = 'logfile', default = 'mmtk.log')
        logfile.label = 'Logfile'   
        
    Mmtk.Inventory = Inventory
except:
    pass
