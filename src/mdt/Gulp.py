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

class Gulp(object):
    '''base class for common gulp runtypes'''
    
    matter = None
    temperature = 300.0
    pressure = 0.0
    forcefield_name='None'
    identify_molecules = 'identify molecules; retain intramolecular Coulomb forces'
    assign_bonds_from_initial_geometry = False
    calc_dispersion_in_recip_space = False
    logfile = 'gulp.log'
    inputfile = 'gulp.gin'
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
    
try:
    from dsaw.model.Inventory import Inventory as InvBase
    from matter.orm.Structure import Structure
    class Inventory(InvBase):
        matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
        matter.label = 'Logfile' 
        temperature = InvBase.d.float(name = 'temperature', default = 300.0)
        temperature.label = 'Temperature or Initial Energy (K)' 
        pressure = InvBase.d.float(name = 'pressure', default = 0.0)
        pressure.label = 'Pressure (GPa)' 
        
        forcefield_name = InvBase.d.str(name = 'forcefield_name', default = 'None')  
        forcefield_name.label = 'Name of Forcefield'
        identify_molecules = InvBase.d.str(name = 'identify_molecules', default = 'identify molecules; retain intramolecular Coulomb forces')
        identify_molecules.label = 'How to Identify Molecules and Calculate Coloumb Forces'
        identify_molecules.validator = InvBase.v.choice(['None','identify molecules; remove intramolecular Coulomb forces',
                                                     'identify molecules; retain intramolecular Coulomb forces'])
        assign_bonds_from_initial_geometry = InvBase.d.bool(name = 'assign_bonds_from_initial_geometry ', default = False)
        assign_bonds_from_initial_geometry.label = 'Assign Bonds from Initial Geometry Only?'
        calc_dispersion_in_recip_space = InvBase.d.bool(name = 'calc_dispersion_in_recip_space', default = False)
        calc_dispersion_in_recip_space.label = 'Calculate Dispersion in Reciprocal Space?'
        
        logfile = InvBase.d.str(name = 'logfile', default = 'gulp.log')
        logfile.label = 'Logfile'    
        inputfile = InvBase.d.str(name = 'inputfile', default = 'gulp.gin')
    Gulp.Inventory = Inventory
except:
    pass
