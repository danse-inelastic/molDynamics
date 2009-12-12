# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from GulpPotential import GulpPotential
from matter.orm.Structure import Structure

class GulpSettings:
    #input
    structure = Structure()
    runtype = 'md'
    dos_projections = [0.]
    potential = GulpPotential()
    description = ''
    inputFile = 'gulp.gin'
    creator = ''
    date = ''
    #results = GulpResults()
    #results
    compressed_xyzTrajectory_filename = 'outputmovie.xyz.zip'
    xyzTrajectory_filename = 'outputmovie.xyz'
    output_filename = 'gulp.gout'
    dos_filename = 'dos.dens'
    

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        return    

