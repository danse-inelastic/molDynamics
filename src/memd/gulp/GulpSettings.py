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
    trajectories = ['gulp.his']
    output_filename = 'gulp.gout'
    dos_filename = 'dos.dens' #don't need to make this user settable

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
           
    class Inventory(InvBase):
        matter = InvBase.d.reference(name='matter', targettype=Structure, owned=False)
        runtype = InvBase.d.str(name = 'runtype', max_length = 80, default = '')
        dos_projection = InvBase.d.array(name='dos_projection', elementtype='float', shape=1, default=[0.0])
        potential = InvBase.d.reference(name='potential', targettype=GulpPotential, owned=False)
        short_description = InvBase.d.str(name = 'short_description', max_length = 80, default = '')
        inputFile = InvBase.d.str(name = 'inputFile', max_length = 80, default ="gulp.gin")
        creator = InvBase.d.str(name = 'creator', max_length = 80, default = '')
#        date = InvBase.d.date(name = 'date')
#        results_state = InvBase.d.str(name='results_state', length=16, default='')
        trajectories = InvBase.d.array(name = 'trajectories', elementtype='str', default = ['gulp.his'])
        output_filename = InvBase.d.str(name = 'output_filename', max_length = 80, default ='gulp.gout')
        dos_filename = InvBase.d.str(name = 'dos_filename', max_length = 80, default ='dos.dens')
        
    def getDOAndOutputFile(self):
        compressedTrajectories = [filename+'.zip' for filename in self.trajectories]
        #based on runtypes 
        outputFiles = {"optimization":{'matter.orm.Structure':None}, 
            "fit":{'memd.gulp.GulpPotential':None},
            "phonons":{'vsat.PhononDOS':self.dos_filename, 
                'vsat.Phonons':['polarizations.pkl', 'energies.pkl']}, 
            "free energy calc/optimize":{'matter.orm.Structure':None},
            "molecular dynamics":{'vsat.Motion':compressedTrajectories}, 
            "monte carlo":{'vsat.PhaseSpaceSample':compressedTrajectories,
                'matter.orm.Structure':None},
            "energetics and material properties":None,
            "surface calc/optimize":{'matter.orm.Structure':None},
            "transition state":None,
            "structure prediction":{'matter.orm.Structure':None}}
        return outputFiles[self.runtype]
        
    def getOutputFiles(self):
        compressedTrajectories = [filename+'.zip' for filename in self.trajectories]
        base = [self.output_filename]
        mdout = base+compressedTrajectories
        phononsout = base+[self.dos_filename,'polarizations.pkl','energies.pkl']
        #dosout = base + 
        #based on runtypes 
        outputFiles = {"optimization":base, 
            "fit":base,
            "phonons":phononsout, 
            "free energy calc/optimize":base,
            "molecular dynamics":mdout, 
            "monte carlo":base,
            "energetics and material properties":base,
            "surface calc/optimize":base,
            "transition state":base,
            "structure prediction":base}
        return outputFiles[self.runtype]



