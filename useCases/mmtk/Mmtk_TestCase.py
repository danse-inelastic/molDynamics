#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from sample.Sample import Sample
from crystal.UnitCell import UnitCell
from crystal.UnitCellBuilder import UnitCellBuilder
from molDynamics.mmtk.Mmtk import Mmtk
from molDynamics.mmtk.AmberForcefield import AmberForcefield
from molDynamics.mmtk.LennardJonesForcefield import LennardJonesForcefield
#from sampleCreation.supercell.Supercell import Supercell
import unittest 
import string



appName = "Mmtk"
caseName = "fulltest"

import journal
debug = journal.debug( "%s-%s" % (appName, caseName) )

class MmtkMd_TestCase(unittest.TestCase):
    '''mmtk test'''
    
    def setUp(self):
        """do argon"""
        argonConfiguration = file('argon.conf')
        lx, ly, lz = map(string.atof, string.split(argonConfiguration.readline()))
        self.material = Structure()
        uc = UnitCell()
        uc.i.a = str(lx)+' 0.0 0.0'
        uc.i.b = '0.0 '+str(ly)+' 0.0'
        uc.i.c = '0.0 0.0 '+str(lz)
        unitCellBuilder = UnitCellBuilder()
        unitCellBuilder.i.unitCell = uc
        atoms = ''
        while 1:
            line = argonConfiguration.readline()
            if not line: break
            atoms+='Ar '+line
        unitCellBuilder.i.atoms = atoms
        self.sample.i.atomicStructure = unitCellBuilder
        self.sample.i.initialTemp = 300.0



    def testMmtkNVE(self):
        #amber = AmberForcefield()
        lennard = LennardJonesForcefield()
        md = Mmtk()
        md.i.sample = self.sample
        md.i.runType = 'md'
        md.i.forcefields = lennard
        md.i.ensemble = 'nve'
        md.i.timestep = 0.5
        md.i.equilibrationTime = 0.005
        md.i.productionTime = 0.4
        md.integrate()
        #print md.getFinalConfiguration()
        
    def testMmtkNVT(self):
        lennard = LennardJonesForcefield()
        self.sample.i.temperature = 200.0
        md = Mmtk()
        md.i.sample = self.sample
        md.i.runType = 'md'
        md.i.forcefields = lennard       
        md.i.ensemble = 'nvt'
        md.i.timestep = 0.5
        md.i.equilibrationTime = 0.005
        md.i.productionTime = 0.01
        md.integrate()
        
    def testMmtkNPT(self):
        self.sample.i.temperature = 300.0
        self.sample.i.pressure = 1.0
        lennard = LennardJonesForcefield()
        md = Mmtk()
        md.i.sample = self.sample
        md.i.runType = 'md'
        md.i.forcefields = lennard  
        md.i.ensemble='npt'
        md.i.timestep=0.5
        md.i.equilibrationTime=0.005
        md.i.productionTime=0.01
        md.integrate()
  
class MmtkRestart_TestCase(unittest.TestCase):
    
    def setUp(self):
        """do argon"""
        argonConfiguration = file('argon.conf')
        lx, ly, lz = map(string.atof, string.split(argonConfiguration.readline()))
        self.sample = Sample('periodic')
        self.sample.unitCell = [[lx, 0.0, 0.0], [0.0, ly, 0.0], [0.0, 0.0, lz]]
        atoms = []
        while 1:
            line = argonConfiguration.readline()
            if not line: break
            x, y, z = map(string.atof, string.split(line))
            atoms.append(['Ar', x, y, z])
        self.sample.atoms = atoms
        self.sample.initialTemp = 300.0
        self.sample.forcefields=[]
        self.sample.forcefields.append(['lennardJonesMmtk',12.0])
        
    def testRestart(self):
        # first do a short md run
        md = Mmtk(self.sample)
        md.i.ensemble = 'nve'
        md.i.timestep = 0.5
        md.i.equilibrationTime = 0.005
        md.i.productionTime = 0.01
        md.i.trajectoryFilename='shortArgonNVE.nc'
        md.i.logFilename='shortArgonNVE.log'
        md.i.restartFilename='shortArgonRestartNVE.nc'
        md.integrate()
        # restart from it
        restartMd = Mmtk(self.sample)
        restartMd.i.restartFilename='shortArgonRestartNVE.nc'
        restartMd.i.logFilename='shortArgonNVE.log'
        restartMd.restartIntegrate()
  
if __name__ == "__main__":
    suite1 = unittest.makeSuite(MmtkMd_TestCase)
    suite2 = unittest.makeSuite(MmtkRestart_TestCase)
    #alltests = unittest.TestSuite((suite1,suite2,suite3))
    alltests = unittest.TestSuite((suite1))
    unittest.TextTestRunner(verbosity=2).run(alltests)
