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
from sample import Units
from mmtk.Mmtk import Mmtk
from ccp1gui.Supercell import Supercell
from os import sep,system
import unittest 
import danseGlob
import string

appName = "Mmtk"
caseName = "fulltest"

import journal
debug = journal.debug( "%s-%s" % (appName, caseName) )

class MmtkNonOrthorhombicMd_TestCase(unittest.TestCase):
    
    def setUp(self):
        """
        do hexagonal argon 2x1x1 supercell from fractional xyz coordinates
        """
        self.lattice=[[2.456, 0.0, 0.0],[-1.228, 2.1269583916945813, 0.0]
                 ,[0.0, 0.0, 6.696]]
        self.fracUnitCell=[['ar', 0.0, 0.0, 0.0], ['ar', 0.0, 0.0, 0.5], 
                        ['ar', 0.33333000000000002, 0.66666999999999998, 0.0], 
                        ['ar', 0.66666999999999998, 0.33333999999999997, 0.5]]
        self.supercellFromFrac=Supercell(self.fracUnitCell,self.lattice,2,1,1)
        self.sample = Sample('periodic')
        self.sample.unitCell = self.supercellFromFrac.getSupercellLatticeVectors()
        self.sample.atoms = self.supercellFromFrac.getSupercellRealCoordinates()
        self.sample.initialTemp = 300.0*Units.K
        self.sample.forcefields=[]
        self.sample.forcefields.append(['lennardJonesMmtk',15.0*Units.Ang])

    def testMmtkNonorthogonal(self):
        md = Mmtk(self.sample)
        md.i.ensemble = 'nve'
        md.i.timestep = 0.5*Units.fs
        md.i.equilibrationTime = 0.005*Units.ps
        md.i.productionTime = 0.1*Units.ps
        md.i.trajectoryFilename='hexagonalMmtk.nc'
        md.i.logFilename='hexagonalMmtk.log'
        md.i.restartFilename='hexagonalRestartMmtk.nc'
        md.integrate()
  
if __name__ == "__main__":
    suite3 = unittest.makeSuite(MmtkNonOrthorhombicMd_TestCase)
    #alltests = unittest.TestSuite((suite1,suite2,suite3))
    alltests = unittest.TestSuite((suite3))
    unittest.TextTestRunner(verbosity=2).run(alltests)
