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

from crystal.UnitCell import UnitCell
from sample.Sample import Sample
from memd.gulp.Gulp import Gulp
from memd.gulp.potentials.TwoAtomPotential import TwoAtomPotential
from os import sep
import unittest 
import string
import os

#appName = "Gulp"
#caseName = "fulltest"
#
#import journal
#debug = journal.debug( "%s-%s" % (appName, caseName) )

def argonSetup(self):
    cwd=os.getcwd()
    argonConfiguration = file(cwd+sep+'argon.conf')
    lx, ly, lz = string.split(argonConfiguration.readline())
    
    self.sample = Sample()
    unitCell=UnitCell()
    unitCell.a=lx+' 0.0 0.0'
    unitCell.b='0.0 '+ly+' 0.0'
    unitCell.c='0.0 0.0 '+lz
    self.sample.i.atomicStructure.i.unitCell = unitCell
    atoms = ''
    atoms.append(argonConfiguration.readline()) #this first line is not parsed anyway so just append at top as 'title'
    while 1:
        line = argonConfiguration.readline()
        if not line: break
#        x, y, z = map(string.atof, string.split(line))
        atoms.append('Ar '+line)
    self.sample.i.atomicStructure.i.atoms = atoms
    self.sample.i.initialTemp = 300.0
    
    self.potential=Potential()
    twoAtom=TwoAtomPotential('Ar','Ar')
    twoAtom.assignInteraction('lennardJonesMmtk')
    #self.sample.forcefieldParameters = twoAtom.getPotential('lennardJonesMmtk')
    self.sample.forcefields=[]
    self.sample.forcefields.append(twoAtom)
    
def tio2Setup(self):
    self.sample = Sample()
    unitCell=UnitCell()
    unitCell.a='4.58666 0.0 0.0'
    unitCell.b='0.0 4.58666 0.0'
    unitCell.c='0.0 0.0 2.95407'
    self.sample.i.atomicStructure.i.unitCell = unitCell

    atoms='''atoms in unit cell
Ti 0.0 0.0 0.0
Ti 2.29333     2.29333     1.477035
O  1.397509435 1.397509435 0.0
O  3.189150565 3.189150565 0.0
O  3.690839435 .8958205646 1.477035000
O  .8958205646 3.690839435 1.477035000
'''
    self.sample.i.atomicStructure.i.atoms = atoms
    self.sample.i.initialTemp = 300.0
    twoAtomTiO=TwoAtomPotential('Ti','O')
    twoAtomTiO.assignInteraction('buckinghamEx23')
    twoAtomOO=TwoAtomPotential('O','O')
    twoAtomOO.assignInteraction('buckinghamEx23')
    #self.sample.forcefieldParameters = twoAtom.getPotential('lennardJonesMmtk')
    self.sample.forcefields=[]
    self.sample.forcefields.append(twoAtomTiO)
    self.sample.forcefields.append(twoAtomOO)
    
  
class GulpMD_TestCase(unittest.TestCase):
    
    def setUp(self):
        """do argon"""
        argonSetup(self)

    def testGulpNVE(self):
        md = Gulp()
        md.i.sample=self.sample
        md.i.potential=self.potential
        md.i.executablePath='/home/brandon/gulp3.0/Src/gulp'
        md.i.ensemble = 'nve'
        md.i.timestep = 0.5
        md.i.equilibrationTime = 0.0001
        md.i.productionTime = 0.001
        md.i.inputDeck='argonNVE.gin'
        md.i.trajectoryFilename='argonNVE.xyz'
        md.i.logFilename='argonNVE.log'
        md.integrate()

    def testGulpNVT(self):
        self.sample.temperature=200.0
        md = Gulp()
        md.i.sample=self.sample
        md.i.ensemble = 'nvt'
        md.i.timestep = 0.5
        md.i.equilibrationTime = 0.0
        md.i.productionTime = 0.001
        md.i.inputDeck='argonNVT.gin'
        md.i.trajectoryFilename='argonNVT.xyz'
        md.i.logFilename='argonNVT.log'
        md.integrate()
        
    def testGulpNPT(self):
        self.sample.temperature=300.0
        self.sample.pressure=0.0001 # 1 atm in GPa
        md = Gulp()
        md.i.sample=self.sample
        md.i.ensemble='npt'
        md.i.timestep=0.5
        md.i.equilibrationTime=0.0
        md.i.productionTime=0.001
        md.i.inputDeck='argonNPT.gin'
        md.i.trajectoryFilename='argonNPT.xyz'
        md.i.logFilename='argonNPT.log'
        md.integrate()

class GulpOpt_TestCase(unittest.TestCase):
    
    def setUp(self):
        """do tiO2 unit cell"""
        tio2Setup(self)
        
    def testOpt(self):
        opt = Gulp()
        opt.i.sample =self.sample
        opt.i.inputDeck='tio2Opt.gin'
        opt.i.trajectoryFilename='tio2Opt.xyz'
        opt.i.logFilename='tio2Opt.log'
        opt.optimize()

    def testOptConstantVolume(self):
        opt = Gulp()
        opt.i.sample=self.sample
        opt.i.constantVolumeOptimize=True
        opt.i.inputDeck='tio2OptConV.gin'
        opt.i.trajectoryFilename='tio2OptConV.xyz'
        opt.i.logFilename='tio2OptConV.log'
        opt.optimize()
        
    def testOptConstantPressure(self):
        opt = Gulp()
        opt.i.sample=self.sample
        opt.i.constantPressureOptimize=True
        opt.i.inputDeck='tio2OptConP.gin'
        opt.i.trajectoryFilename='tio2OptConP.xyz'
        opt.i.logFilename='tio2OptConP.log'
        opt.optimize()

class GulpRestart_TestCase(unittest.TestCase):
    
    def setUp(self):
        """do argon"""
        argonSetup(self)
        
#        cwd=os.getcwd()
#        argonConfiguration = file(cwd+sep+'argon.conf')
#        lx, ly, lz = map(string.atof, string.split(argonConfiguration.readline()))
#        self.sample = Sample()
#        self.sample.unitCell = [[lx, 0.0, 0.0], [0.0, ly, 0.0], [0.0, 0.0, lz]]
#        atoms = []
#        while 1:
#            line = argonConfiguration.readline()
#            if not line: break
#            x, y, z = map(string.atof, string.split(line))
#            atoms.append(['Ar', x, y, z])
#        self.sample.atoms = atoms
#        self.sample.initialTemp = 300.0
#        twoAtom=TwoAtomPotential('Ar','Ar')
#        twoAtom.assignInteraction('lennardJonesMmtk')
#        #self.sample.forcefieldParameters = twoAtom.getPotential('lennardJonesMmtk')
#        self.sample.forcefields=[]
#        self.sample.forcefields.append(twoAtom)
        
    def testRestart(self):
        # first do a short md run
        md = Gulp()
        md.i.sample=self.sample
        md.i.ensemble = 'nve'
        md.i.timestep = 0.5
        md.i.equilibrationTime = 0.0001
        md.i.productionTime = 0.001
        md.i.inputDeck='shortArgonNVE.gin'
        md.i.trajectoryFilename='shortArgonNVE.xyz'
        md.i.logFilename='shortArgonNVE.log'
        md.i.restartFilename='shortArgonNVE.res'
        md.integrate()
        # restart from it
        restartMd = Gulp()
        restartMd.i.sample = self.sample
        restartMd.i.inputDeck='shortArgonNVE.res'
        restartMd.i.logFilename='shortArgonNVE.log'
        restartMd.restartIntegrate()

class GulpFit_TestCase(unittest.TestCase):
    
    def setUp(self):
        """do tiO2 unit cell"""
        self.sample = Sample()
        self.sample.unitCell = [[4.58666, 0.0, 0.0], 
                                [0.0, 4.58666, 0.0], 
                                [0.0, 0.0, 2.95407]]
        atoms=[['Ti', 0.0, 0.0, 0.0],
        ['Ti', 2.29333,     2.29333,     1.477035],
        ['O',  1.397509435, 1.397509435, 0.0],
        ['O',  3.189150565, 3.189150565, 0.0],
        ['O',  3.690839435, .8958205646, 1.477035000],
        ['O',  .8958205646, 3.690839435, 1.477035000]]
        self.sample.atoms = atoms
        self.sample.initialTemp = 300.0
        twoAtomTiO=TwoAtomPotential('Ti','O')
        twoAtomTiO.assignInteraction('buckinghamEx23')
        twoAtomTiO.i.AFit=False
        twoAtomTiO.i.rhoFit=True
        twoAtomTiO.i.AFit=False
        twoAtomOO=TwoAtomPotential('O','O')
        twoAtomOO.assignInteraction('buckinghamEx23')
        #self.sample.forcefieldParameters = twoAtom.getPotential('lennardJonesMmtk')
        self.sample.forcefields=[]
        self.sample.forcefields.append(twoAtomTiO)
        self.sample.forcefields.append(twoAtomOO)
        
    def testFit(self):
        fit = Gulp()
        fit.i.sample=self.sample
        fit.i.inputDeck='tio2Fit.gin'
        fit.i.trajectoryFilename='tio2Fit.xyz'
        fit.i.logFilename='tio2Fit.log'
        fit.fit()

    def testFitConstantVolume(self):
        fit = Gulp()
        fit.i.sample=self.sample
        fit.i.constantVolumeFit=True
        fit.i.inputDeck='tio2FitConV.gin'
        fit.i.trajectoryFilename='tio2FitConV.xyz'
        fit.i.logFilename='tio2FitConV.log'
        fit.fit()
        
    def testFitConstantPressure(self):
        fit = Gulp()
        fit.i.sample=self.sample
        fit.i.constantPressureFit=True
        fit.i.inputDeck='tio2FitConP.gin'
        fit.i.trajectoryFilename='tio2FitConP.xyz'
        fit.i.logFilename='tio2FitConP.log'
        fit.fit()

if __name__ == "__main__":
    suite1 = unittest.makeSuite(GulpMD_TestCase)
    suite2 = unittest.makeSuite(GulpOpt_TestCase)
    suite3 = unittest.makeSuite(GulpFit_TestCase)
    suite4 = unittest.makeSuite(GulpRestart_TestCase)
    alltests = unittest.TestSuite((suite1,suite2,suite3,suite4))
    #alltests = unittest.TestSuite((suite4))
    unittest.TextTestRunner(verbosity=2).run(alltests)

