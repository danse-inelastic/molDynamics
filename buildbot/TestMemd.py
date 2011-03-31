"""Unit tests for analyses tests.
"""
from numpy.ma.testutils import assert_almost_equal, assert_array_almost_equal
import os, sys
import unittest
import numpy

# useful variables
thisfile = locals().get('__file__', 'TestMemd.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
#testdata_dir = os.path.join(tests_dir, 'testdata')

sys.path.insert(0,os.path.abspath('..'))# this should put the source code first on the path

engineTest=True
lim=0

class TestMemd(unittest.TestCase):
    """test gulp and mmtk bindings...
    """

    def setUp(self):
        pass
        
    def testOptimizeApi(self):
        from memd.gulp.Optimize import Optimize
        m = Optimize()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.constraints='constant volume'
        m.inputDeckName = 'mOpt.gin'
        m.trajectoryFilename = 'opt.xyz'
        m.optimizeCoordinates = True
        m.writeInputfile(tests_dir)
        correctInput="""conv optimise 
vectors
2.456 0.0 0.0
0.0 2.456 0.0
0.0 0.0 6.696
cartesian
C   0 0 0
C   0 0 3.348
C   0.708986 1.228 0
C   1.41797 0 3.348
harmonic 
C C 22.594 0.63952 0.0 0.0 1.8
C C  8.301 3.42180 0.0 1.8 2.6
C C -0.231 24.95086 0.0 2.6 3.1
C C  0.362 2.94862 0.0 3.1 3.5
                
supercell 1 1 1
output movie xyz opt.xyz
dump molDynamics.res"""
        # this tests input file
        inputContents=file('mOpt.gin').read().strip()
        #print correctInput[lim:]
        #print inputContents[lim:]
        assert correctInput==inputContents
        # this tests whether parnasis runs with this input file
        inp = os.path.join(tests_dir,'mOpt.gin')
        out = os.path.join(tests_dir,'mOpt.gout')
        if engineTest:
            os.system('gulp < '+inp+' > '+out)

    def testPhononApi(self):
        from memd.gulp.Phonon import Phonon
        m = Phonon()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.kpointMesh = '2 2 2'
        m.broadenDos = True
        m.dosAndDispersionFilename = 'graphitePhonons'
        m.inputDeckName = 'mPhon.gin'
        m.writeInputfile(tests_dir)
        correctInput="""phonon broaden_dos 
vectors
2.456 0.0 0.0
0.0 2.456 0.0
0.0 0.0 6.696
cartesian
C   0 0 0
C   0 0 3.348
C   0.708986 1.228 0
C   1.41797 0 3.348
harmonic 
C C 22.594 0.63952 0.0 0.0 1.8
C C  8.301 3.42180 0.0 1.8 2.6
C C -0.231 24.95086 0.0 2.6 3.1
C C  0.362 2.94862 0.0 3.1 3.5
                
supercell 1 1 1
shrink 2 2 2
project 0
output phonon graphitePhonons
output frequency graphitePhonons"""
        # this tests input file
        inputContents=file('mPhon.gin').read().strip()
        assert correctInput==inputContents
        inp = os.path.join(tests_dir,'mPhon.gin')
        out = os.path.join(tests_dir,'mPhon.gout')
        if engineTest:
            os.system('gulp < '+inp+' > '+out)
            
    def testMdApi(self):
        from memd.gulp.Md import Md
        m = Md()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.temperature = 500
        m.timeStep = 0.002
        m.ensemble = 'nvt'
        m.thermostatParameter=0.05
        m.equilibrationTime = 1
        m.productionTime = 1
        m.propCalcInterval = 0.5
        m.trajectoryFilename = 'mMd.his'
        m.restartFilename = 'mMid.res'
        m.dumpInterval = 0.5
        m.inputDeckName = 'mMd.gin'
        m.writeInputfile(tests_dir)
        correctInput="""md conv 
vectors
2.456 0.0 0.0
0.0 2.456 0.0
0.0 0.0 6.696
cartesian
C   0 0 0
C   0 0 3.348
C   0.708986 1.228 0
C   1.41797 0 3.348
harmonic 
C C 22.594 0.63952 0.0 0.0 1.8
C C  8.301 3.42180 0.0 1.8 2.6
C C -0.231 24.95086 0.0 2.6 3.1
C C  0.362 2.94862 0.0 3.1 3.5
                
supercell 1 1 1
ensemble nvt 0.05
temperature 500
equilibration 1 ps
production 1 ps
timestep 0.002 ps
sample 0.5 ps
output history mMd.his
write 0.5 ps
dump mMid.res"""
        # this tests input file
        inputContents=file('mMd.gin').read().strip()
        assert correctInput==inputContents 
        inp = os.path.join(tests_dir,'mMd.gin')
        out = os.path.join(tests_dir,'mMd.gout')
        if engineTest:
            os.system('gulp < '+inp+' > '+out)

if __name__ == '__main__':
    unittest.main()

