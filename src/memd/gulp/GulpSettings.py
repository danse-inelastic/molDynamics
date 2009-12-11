# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
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
    

# version
__id__ = "$Id$"

# End of file 
