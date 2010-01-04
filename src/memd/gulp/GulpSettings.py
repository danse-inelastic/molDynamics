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
#from matter.orm.AtomicStructure import Structure
from matter.orm.Structure import Structure
from dsaw.model.Inventory import Inventory as InvBase

class GulpSettings:
    #input
    structure = Structure()
    runtype = 'md'
    dos_projection = [0.0]
    potential = GulpPotential()
    description = ''
    inputFile = 'gulp.gin'
    creator = ''
    #date = ''
    #results = GulpResults()
    #results
    compressed_xyzTrajectory_filename = 'outputmovie.xyz.zip'
    xyzTrajectory_filename = 'outputmovie.xyz'
    output_filename = 'gulp.gout'
    dos_filename = 'dos.dens'

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
           
    class Inventory(InvBase):
        structure = InvBase.d.reference(name='structure', targettype=Structure, owned=False)
        runtype = InvBase.d.str(name = 'runtype', max_length = 80, default ="md")
        dos_projection = InvBase.d.array(name='dos_projection', elementtype='float', shape=1)
        potential = InvBase.d.reference(name='potential', targettype=GulpPotential, owned=False)
        description = InvBase.d.str(name = 'description', max_length = 80, default ="")
        inputFile = InvBase.d.str(name = 'inputFile', max_length = 80, default ="gulp.gin")
        creator = InvBase.d.str(name = 'creator', max_length = 80, default ="")
        #date = InvBase.d.str(name = 'date', max_length = 80, default ="")
        compressed_xyzTrajectory_filename = InvBase.d.str(name = 'compressed_xyzTrajectory_filename', 
                                                                 max_length = 80, default ='outputmovie.xyz.zip')
        xyzTrajectory_filename = InvBase.d.str(name = 'xyzTrajectory_filename', max_length = 80, default ='outputmovie.xyz')
        output_filename = InvBase.d.str(name = 'output_filename', max_length = 80, default ='gulp.gout')
        dos_filename = InvBase.d.str(name = 'dos_filename', max_length = 80, default ='dos.dens')


