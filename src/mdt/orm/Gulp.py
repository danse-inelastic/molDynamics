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

from ..Gulp import Gulp

from dsaw.model.Inventory import Inventory as InvBase
from matter.orm.Structure import Structure
from memd.gulp.GulpPotential import GulpPotential
class Inventory(InvBase):
    matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
    matter.label = 'Structure' 
    temperature = InvBase.d.float(name = 'temperature', default = 300.0)
    temperature.label = 'Temperature or Initial Energy (K)' 
    pressure = InvBase.d.float(name = 'pressure', default = 0.0)
    pressure.label = 'Pressure (GPa)' 
    #        forcefield_name = InvBase.d.str(name = 'forcefield_name', default = 'None')  
    #        forcefield_name.label = 'Name of Forcefield'
    forcefield = InvBase.d.reference(name='forcefield', targettype=GulpPotential, owned=False)
    forcefield.label = 'Name of Forcefield'
    identify_molecules = InvBase.d.str(name = 'identify_molecules', default = 'identify molecules; retain intramolecular Coulomb forces')
    identify_molecules.label = 'How to Identify Molecules and Calculate Coulomb Forces'
    identify_molecules.validator = InvBase.v.choice(['None','identify molecules; remove intramolecular Coulomb forces',
                                                     'identify molecules; retain intramolecular Coulomb forces'])
    assign_bonds_from_initial_geometry = InvBase.d.bool(name = 'assign_bonds_from_initial_geometry', default = False)
    assign_bonds_from_initial_geometry.label = 'Assign Bonds from Initial Geometry Only?'
    calc_dispersion_in_recip_space = InvBase.d.bool(name = 'calc_dispersion_in_recip_space', default = False)
    calc_dispersion_in_recip_space.label = 'Calculate Dispersion in Reciprocal Space?'

    # XXX: not really necessary to have filenames in the db. 
    # XXX: it is not "essential" information required for simulation.
    # XXX: the original reason of having them is to allow users to assign different names
    # XXX: to avoid name confliction. but the db record id is the identifier that should
    # XXX: be good enough. And it could be cleaner to keep simulations at different
    # XXX: subdirs. Even if it is needed to have files in one flat directory,
    # XXX: it would be no problem to have a script to do the renaming.
    # logfile = InvBase.d.str(name = 'logfile', default = 'gulp.log')
    # logfile.label = 'Logfile'    
    # inputfile = InvBase.d.str(name = 'inputfile', default = 'gulp.gin')

Gulp.Inventory = Inventory
