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

class Gulp(object):
    '''base class for common gulp runtypes'''
    
    matter = None
    supercell = '1 1 1'
    temperature = 300.0
    pressure = 0.0
    # forcefield_name='None'
    forcefield = None
    identify_molecules = 'identify molecules; retain intramolecular Coulomb forces'
    assign_bonds_from_initial_geometry = False
    calc_dispersion_in_recip_space = False
    logfile = 'gulp.log'
    inputfile = 'gulp.gin'
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
    
