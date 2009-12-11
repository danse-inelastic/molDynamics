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
from GulpResults import GulpResults
from matter.Structure import Structure

class GulpSettings:

    runtype = 'md'
    dos_projections = []
    potential = GulpPotential()
    description = ''
    inputFile = 'gulp.gin'
    creator = ''
    date = ''
    results = GulpResults()
    structure = Structure()

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        return    

