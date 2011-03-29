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

parnasisTest=False
lim=100

class TestAtomSimulation(unittest.TestCase):
    """test gulp and mmtk bindings...note we remove first 100 characters to get rid of date info
    ...also note we have a switch to also test parnasis engine above
    """

    def setUp(self):
        from vsat.Trajectory import Trajectory
        ncFilePath = '5MF6SB7Q/gulp.nc'
        self.traj = Trajectory(filename=ncFilePath)
        self.traj.loadNetcdfTrajectory()
        
    def testEisfApi(self):
        """test EISF"""
        from vsat.trajectory.EisfCalc import EisfCalc
        eisfc = EisfCalc()
        eisfc.trajectory = self.traj
        eisfc.q_range = [0,2]
        eisfc.q_resolution = 0.1
        eisfc.time_steps_sampled = (0, 165, 1) 
        eisfc.selected_atoms = {'Au': 'All'}
        eisfc.writeInputFile()
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
        inputContents=file('eisf.inp').read().strip()
        #print correctInput[lim:]
        #print inputContents[lim:]
        assert correctInput[lim:]==inputContents[lim:]
        # this tests whether parnasis runs with this input file
        if parnasisTest:
            from parnasis.ParnasisApp import ParnasisApp
            p = ParnasisApp()
            p.singleRun('eisf.inp')

    def testMdDosApi(self):
        """test MdDos"""
        from vsat.trajectory.MdDosCalc import MdDosCalc
        mdc = MdDosCalc()
        mdc.trajectory = self.traj
        mdc.time_steps_sampled = (0, 165, 1) 
        mdc.selected_atoms = {'Au': 'All'}
        mdc.writeInputFile()
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
        inputContents=file('mddos.inp').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if parnasisTest:
            from parnasis.ParnasisApp import ParnasisApp
            p = ParnasisApp()
            p.singleRun('mddos.inp')
            
    def testMsdDiffusionApi(self):
        """test MsdDiffusion"""
        from vsat.trajectory.MsdDiffusionCalc import MsdDiffusionCalc
        msdc = MsdDiffusionCalc()
        msdc.trajectory = self.traj
        msdc.time_steps_sampled = (0, 165, 1) 
        msdc.selected_atoms = {'Au': 'All'}
        msdc.writeInputFile()
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
        if parnasisTest:
            from parnasis.ParnasisApp import ParnasisApp
            p = ParnasisApp()
            p.singleRun('msddiffusion.inp')


    def testCsfApi(self):
        """test Csf"""
        from vsat.trajectory.FCsfCalc import FCsfCalc
        csf = FCsfCalc()
        csf.trajectory = self.traj
        csf.q_range = [0, 5]
        csf.q_resolution = 0.1
        csf.time_steps_sampled = (0, 165, 1) 
        csf.selected_atoms = {'Au': 'All'}
        csf.writeInputFile()
        correctInput="""#
# parnasis data
# Created by: jbk
# Date of creation: Mon Mar 21 23:19:01 2011
#
q_algorithm = 'random_gen' 
q_type = 'powder average' 
q_resolution = 0.1 
trajectory = ['5MF6SB7Q/gulp.nc'] 
time_steps_sampled = (0, 165, 1) 
selected_atoms = {'Au': ['*']} 
q_range = [0, 5] 
short_description = 'coherent S(Q,E)' 
weights = 'coherent' 
q_directions = [True, True, True] 
type = 'fcsf' 
output_files = {'fcsf': 'FCSF_gulp.nc', 'fft': 'FCSF_SPECT_gulp.nc'}"""
        # this tests input file
        inputContents=file('fcsf.inp').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if parnasisTest:
            from parnasis.ParnasisApp import ParnasisApp
            p = ParnasisApp()
            p.singleRun('fcsf.inp')

    def testMeCsfApi(self):
        from vsat.trajectory.MeCsfCalc import MeCsfCalc
        mecsf = MeCsfCalc()
        mecsf.trajectory = self.traj
        mecsf.q_range = [0, 8]
        mecsf.q_resolution = 0.01
        mecsf.time_steps_sampled = (0, 165, 1) 
        mecsf.selected_atoms = {'Au': 'All'}
        mecsf.writeInputFile()
        correctInput="""#
# parnasis data
# Created by: jbk
# Date of creation: Mon Mar 21 23:28:19 2011
#
q_algorithm = 'random_gen' 
q_type = 'powder average' 
q_resolution = 0.01 
me_order = 50 
trajectory = ['5MF6SB7Q/gulp.nc'] 
time_steps_sampled = (0, 165, 1) 
selected_atoms = {'Au': ['*']} 
me_precision = 'None' 
q_range = [0, 8] 
short_description = 'maximum entropy coherent S(Q,E)' 
weights = 'coherent' 
q_directions = [True, True, True] 
type = 'mecsf' 
output_files = {'memory': 'ME-CSF_Memory_gulp.nc', 'fft': 'ME-CSF_SPECT_gulp.nc', 'mecsf': 'ME-CSF_gulp.nc'}"""
        # this tests input file
        inputContents=file('mecsf.inp').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if parnasisTest:
            from parnasis.ParnasisApp import ParnasisApp
            p = ParnasisApp()
            p.singleRun('mecsf.inp')
            
    def testVacfDiffusionApi(self):
        from vsat.trajectory.VacfDiffusionCalc import VacfDiffusionCalc
        vacf = VacfDiffusionCalc()
        vacf.trajectory = self.traj
        vacf.time_steps_sampled = (0, 165, 1) 
        vacf.selected_atoms = {'Au': 'All'}
        vacf.writeInputFile()
        correctInput="""#
# parnasis data
# Created by: jbk
# Date of creation: Mon Mar 21 23:33:27 2011
#
trajectory = ['5MF6SB7Q/gulp.nc'] 
time_steps_sampled = (0, 165, 1) 
selected_atoms = {'Au': ['*']} 
weights = 'mass' 
short_description = 'Vacf diffusion calculation' 
type = 'vacfdiffusion' 
output_files = {'plot': 'VACF_gulp.plot'}"""
        # this tests input file
        inputContents=file('vacfdiffusion.inp').read().strip()
        assert correctInput[lim:]==inputContents[lim:] 
        # this tests whether parnasis runs with this input file
        if parnasisTest:
            from parnasis.ParnasisApp import ParnasisApp
            p = ParnasisApp()
            p.singleRun('vacfdiffusion.inp')

if __name__ == '__main__':
    unittest.main()

