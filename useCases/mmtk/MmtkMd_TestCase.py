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
from memd.mmtk.Mmtk import Mmtk
from memd.mmtk.AmberForcefield import AmberForcefield
from memd.mmtk.LennardJonesForcefield import LennardJonesForcefield
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
        """do iron supercell"""
        at1 = Atom('Fe', [0,0,0])
        at2 = Atom('Fe', [0.5,0.5,0.5])
        self.stru = Structure( [ at1, at2], lattice=Lattice(2.87, 2.87, 2.87, 90, 90, 90) )       
        self.sample = Sample()
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
        self.sample.i.temperature=200.0
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
        self.sample.i.temperature=300.0
        self.sample.i.pressure=1.0
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
  
  
if __name__ == "__main__":
    unittest.main()
