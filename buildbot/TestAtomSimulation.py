"""Unit tests for analyses tests.
"""
from numpy.ma.testutils import assert_almost_equal, assert_array_almost_equal
import os, sys
import unittest
import numpy

# useful variables
thisfile = locals().get('__file__', 'TestAtomSimulation.py')
tests_dir = os.path.dirname(os.path.abspath(thisfile))
#testdata_dir = os.path.join(tests_dir, 'testdata')

sys.path.insert(0,os.path.abspath('..'))# this should put the source code first on the path

engineTest=False
lim=100

class TestAtomSimulation(unittest.TestCase):
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
        correctInput="""#
# parnasis data
# Created by: jbk
# Date of creation: Mon Mar 21 11:18:33 2011
#
q_algorithm = 'random_gen' 
q_type = 'powder average' 
q_resolution = 0.1 
trajectory = ['5MF6SB7Q/gulp.nc'] 
time_steps_sampled = (0, 165, 1) 
selected_atoms = {'Au': ['*']} 
q_range = [0, 2] 
short_description = 'EISF' 
weights = 'incoherent' 
q_directions = [True, True, True] 
type = 'eisf' 
output_files = {'eisf': 'EISF_gulp.plot'}"""
        # this tests input file
        inputContents=file('mOpt.gin').read().strip()
        #print correctInput[lim:]
        #print inputContents[lim:]
        assert correctInput[lim:]==inputContents[lim:]
        # this tests whether parnasis runs with this input file
        if engineTestTest:
            os.system('gulp < mdOpt.gin > mdOpt.gout')

    def testPhononApi(self):
        from memd.gulp.Phonon import Phonon
        m = Phonon()
        m.xyzFile='structure.xyz'
        m.forcefield='axiallySymmetricNWS.lib'
        m.inputDeckName = 'mPhon.gin'
        m.writeInputfile(tests_dir)
        correctInput="""#
# parnasis data
# Created by: jbk
# Date of creation: Mon Mar 21 11:59:33 2011
#
trajectory = ['5MF6SB7Q/gulp.nc'] 
smoothing_window = 1 
time_steps_sampled = (0, 165, 1) 
selected_atoms = {'Au': ['*']} 
weights = 'mass' 
short_description = 'DOS calculation' 
smoothing_type = 'hanning' 
type = 'mddos' 
output_files = {'dos': 'DOS_gulp.plot'}"""
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
        correctInput="""#
# parnasis data
# Created by: jbk
# Date of creation: Mon Mar 21 19:19:38 2011
#
diffusion_time_steps = 'All' 
dimensions = 3 
trajectory = ['5MF6SB7Q/gulp.nc'] 
time_steps_sampled = (0, 165, 1) 
selected_atoms = {'Au': ['*']} 
weights = 'mass' 
short_description = 'mean squared displacement' 
type = 'msddiffusion' 
projection_vector = 'None' 
output_files = {'diffusion': 'DIFFUSION_gulp.plot', 'msd': 'MSD_gulp.plot'}"""
        # this tests input file
        inputContents=file('msddiffusion.inp').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if engineTest:
            os.system('gulp < mMd.gin > mMd.gout')

if __name__ == '__main__':
    unittest.main()

