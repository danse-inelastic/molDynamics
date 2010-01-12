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
    matter = Structure() 
    runtype = ''
    dos_projection = [0.0]
    potential = GulpPotential()
    inputFile = 'gulp.gin'
    
    short_description = ''
    creator = ''
#    import time
#    date = time.ctime()
#    results_state = ''
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
        matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
        runtype = InvBase.d.str(name = 'runtype', max_length = 80)
        dos_projection = InvBase.d.array(name='dos_projection', elementtype='float', shape=1)
        potential = InvBase.d.reference(name='potential', targettype=GulpPotential, owned=False)
        short_description = InvBase.d.str(name = 'short_description', max_length = 80)
        inputFile = InvBase.d.str(name = 'inputFile', max_length = 80, default ="gulp.gin")
        
        creator = InvBase.d.str(name = 'creator', max_length = 80)
#        date = InvBase.d.date(name = 'date')
#        results_state = InvBase.d.str(name='results_state', length=16, default='')
        compressed_xyzTrajectory_filename = InvBase.d.str(name = 'compressed_xyzTrajectory_filename', 
                                                                 max_length = 80, default ='outputmovie.xyz.zip')
        xyzTrajectory_filename = InvBase.d.str(name = 'xyzTrajectory_filename', max_length = 80, default ='outputmovie.xyz')
        output_filename = InvBase.d.str(name = 'output_filename', max_length = 80, default ='gulp.gout')
        dos_filename = InvBase.d.str(name = 'dos_filename', max_length = 80, default ='dos.dens')
        
        



