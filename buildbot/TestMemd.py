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

engineTest=False
lim=100

class TestMemd(unittest.TestCase):
    """test gulp and mmtk bindings...note we remove first 100 characters to get rid of date info
    ...also note we have a switch to also test parnasis engine above
    """

    def setUp(self):
        pass
        
    def testOptimizeApi(self):
        from memd.gulp.Optimize import Optimize
        m = Optimize()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.inputDeckName = 'mOpt.gin'
        m.writeInputfile(tests_dir)
        correctInput="""optimise 
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
                
output movie xyz molDynamics.xyz
dump molDynamics.res"""
        # this tests input file
        inputContents=file('mOpt.gin').read().strip()
        #print correctInput[lim:]
        #print inputContents[lim:]
        assert correctInput[lim:]==inputContents[lim:]
        # this tests whether parnasis runs with this input file
        if engineTest:
            os.system('gulp < mdOpt.gin > mdOpt.gout')

    def testPhononApi(self):
        from memd.gulp.Phonon import Phonon
        m = Phonon()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.inputDeckName = 'mPhon.gin'
        m.writeInputfile(tests_dir)
        correctInput="""phonon 
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
                
shrink 
project 0
output phonon 
output frequency"""
        # this tests input file
        inputContents=file('mPhon.gin').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if engineTest:
            os.system('gulp < mPhon.gin > mPhon.gout')
            
    def testMdApi(self):
        from memd.gulp.Md import Md
        m = Md()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
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
                
ensemble nvt 0.05
temperature 0.0
equilibration 0.0 ps
production 0.0 ps
timestep 0.002 ps
sample 5.0 ps
output history molDynamics.his.his
write 0.0 ps
dump molDynamics.res"""
        # this tests input file
        inputContents=file('mMd.gin').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if engineTest:
            os.system('gulp < mMd.gin > mMd.gout')

if __name__ == '__main__':
    unittest.main()

