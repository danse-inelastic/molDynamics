#!/usr/bin/env python
# =================================================================
#
# {LicenseText}
#
# =================================================================
#

from memd.MolDynamics import MolDynamics
import math
import MMTK
from MMTK import Units
from MMTK.ForceFields import LennardJonesForceField, Amber94ForceField
from MMTK.Environment import NoseThermostat, AndersenBarostat
from MMTK.Trajectory import Trajectory, TrajectoryOutput, LogOutput, RestartTrajectoryOutput
from MMTK.Dynamics import VelocityVerletIntegrator, VelocityScaler, \
                          TranslationRemover, RotationRemover,BarostatReset
from os import linesep
  
class Mmtk(MolDynamics):
    """MMTK functionality usable in DANSE.
    
This class maps the API to MMTK commands and executes them."""

    class Inventory(MolDynamics.Inventory):
        import pyre.inventory as inv 
        integrator = inv.str('integrator', default = 'velocity-verlet')
        integrator.meta['tip'] = 'type of integrator'
        
        runType = inv.str('runType', default = 'md')
        runType.validator = inv.choice(['md', 'restart md'])
        runType.meta['tip'] = 'type of run'
        
        forcefield = inv.facility('forcefield', default = 'amber')
        forcefield.meta['known_plugins']=['amber', 'lennardJones']
        forcefield.meta['tip'] = 'type of forcefield'
                
        barostatParameter = inv.float('Barostat Parameter', default = 0.005)
        barostatParameter.meta['tip'] = '''barostat parameter to keep fluctuations relatively small'''
        
        ensemble = inv.str('Thermodynamic Ensemble', default = 'nve') 
        ensemble.validator = inv.choice(["nve", "nvt", "npt"])
        ensemble.meta['tip'] = 'thermodynamic ensemble (nve, nvt, npt, ...)'
        
        equilibrationTime = inv.float('Equilibration Time (ps)', default = 0.0)
        equilibrationTime.meta['tip'] = 'equilibration time of the simulation (ps)'
        
        productionTime = inv.float('Production Time (ps)', default = 5.0)
        productionTime.meta['tip'] = 'production time of the simulation'
        
        sampleFrequency = inv.float('Properties Calculation Frequency (fs)', default = 5.0)
        sampleFrequency.meta['tip'] = '''frequency at which sampled properties are 
written to trajectory and log file'''
        
        thermostatParameter = inv.float('Thermostat Parameter', default = 0.005)
        thermostatParameter.meta['tip'] = '''thermostat parameter to keep 
fluctuations relatively small'''
        
        timeStep = inv.float('Time step (fs)', default = 0.5)
        timeStep.meta['tip'] = 'integration time step (ps)'
        
        trajectoryFilename = inv.str('Trajectory Filename', default='molDynamics')
        trajectoryFilename.meta['tip'] = 'name of trajectory file(s)'

        restartFilename = inv.str('Restart Filename', default = 'molDynamics.res')
        restartFilename.meta['tip'] = '''restart file for resuming an md run or optimization'''
        
        dumpFrequency = inv.float('Dump Frequency (ps)', default = 0.0)
        dumpFrequency.meta['tip'] = '''frequency at which a restart file is written'''

        trajectoryType = inv.str('Trajectory Type', default='xyz')
        trajectoryType.meta['tip'] = 'type of trajectory output'  
        trajectoryType.validator = inv.choice(['xyz', 'history', 'xyz and history'])

    def __init__(self, name='mmtk'):
        MolDynamics.__init__(self, name, 'engine')
        #self._setDefaults()
        self.mmtkUniverse = None
        
#    def _setDefaults(self):
#        '''set defaults specific to mmtk'''
#        self.inventory.trajectoryFilename = 'molDynamics.nc'
#        self.inventory.restartFilename = 'restart.nc'
#        self.inventory.sampleFrequency = self.inventory.timeStep*Units.fs
#        self.inventory.dumpFrequency = self.inventory.timeStep*Units.fs
        
    def _norm(self,vec):
        """gives the Euclidean _norm of a list"""
        temp=sum([el**2. for el in vec])
        return math.sqrt(temp)
        
    def _ind(self,list):
        """gives the indices of the list to iterate over"""
        return range(len(list))
        
    def _dot(self,v1,v2):
        """returns the _dot product of v1 and v2"""
        return sum([v1[i]*v2[i] for i in self._ind(v1)])
        
    def _vecsToParams(self,vecs):
        """takes lattice vectors in cartesian coordinates with origin at {0,0,0}
        and returns lattice parameters"""
        conv=math.pi/180
        [a,b,c]=vecs
        ma=math.sqrt(self._dot(a,a))
        mb=math.sqrt(self._dot(b,b))
        mc=math.sqrt(self._dot(c,c))
        al=1/conv*math.acos(self._dot(b,c)/mb/mc)
        be=1/conv*math.acos(self._dot(a,c)/ma/mc)
        ga=1/conv*math.acos(self._dot(a,b)/ma/mb)
        return [ma, mb, mc, al, be, ga]
    
    def appEqual(self,v1,v2):
        '''equal to within a certain numerical accuracy'''
        if v1-v2<10**-6:
            return True
        else:
            return False
        
    def _setForcefield(self):
        '''This function sets the forcefield.'''
        self.ff=self.inventory.forcefield.getForcefield()
        
    def _setInitialConditions(self):
        '''map MolDynamics unit cell stuff to MMTK's. 
        Eventually much of this will be taken by the crystal class''' 
        atoms = self.inventory.sample.getAtomsAsStrings()
        uc = self.inventory.sample.getCellVectors()
        if uc==None:
            self.mmtkUniverse = MMTK.InfiniteUniverse(self.ff)
        else:
            #ucList=uc.tolist()
            (a,b,c,al,be,ga)=self._vecsToParams(uc)
            if self.appEqual(al, 90.0) and self.appEqual(be, 90.0) and self.appEqual(ga, 90.0):
                if a==b and b==c:
                    self.mmtkUniverse = MMTK.CubicPeriodicUniverse(a*Units.Ang, self.ff)
                else:
                    self.mmtkUniverse = MMTK.OrthorhombicPeriodicUniverse(
                            (a*Units.Ang, b*Units.Ang, c*Units.Ang), self.ff)
            else:
                uc = self.inventory.sample.unitCell
                self.mmtkUniverse = MMTK.ParallelepipedicPeriodicUniverse(
                    ((uc[0][0]*Units.Ang, uc[0][1]*Units.Ang, uc[0][2]*Units.Ang),
                     (uc[1][0]*Units.Ang, uc[1][1]*Units.Ang, uc[1][2]*Units.Ang),
                     (uc[2][0]*Units.Ang, uc[2][1]*Units.Ang, uc[2][2]*Units.Ang)), self.ff)
        #add objects to mmtkUniverse
        for atom in atoms:
            species, x, y, z = atom.split()
            self.mmtkUniverse.addObject(MMTK.Atom(species, position = \
                MMTK.Vector(float(x)*Units.Ang, float(y)*Units.Ang, float(z)*Units.Ang))) 
#        elif self.inventory.sample.has_attribute('molecule'):
#            pass
        
    def createTrajectoryAndIntegrator(self):
        '''create trajectory and integrator'''
        #initialize velocities--this has to happen after adding atoms
        self.mmtkUniverse.initializeVelocitiesToTemperature(self.inventory.sample.i.temperature)
        # Create trajectory and integrator.
        self.mmtkTrajectory = Trajectory(self.mmtkUniverse, self.inventory.trajectoryFilename, "w")
        self.mmtkIntegrator = VelocityVerletIntegrator(self.mmtkUniverse, delta_t=self.inventory.timeStep*Units.fs)
        # Periodical actions for equilibration output.
        self.equilibration_actions = [TranslationRemover(0, None, 100),
            RotationRemover(0, None, 100),
            LogOutput(self.inventory.logFilename, ('time', 'energy'), 0, None)
            ]  
        # Periodical actions for trajectory output and text log output.
        self.output_actions = [TrajectoryOutput(self.mmtkTrajectory,
            ('configuration', 'energy', 'thermodynamic', 'time', 'auxiliary'), 
            0, None, 20), #TODO: Fixme so the user can specify when trajectory and sample frequency happens
            #this last option makes it so none of the equilibration steps are output, consistent with Gulp
            LogOutput(self.inventory.logFilename, ('time', 'energy'), 0, None, 20) #this last 0 makes it so all equilibration steps are output, consistent with Gulp
            ]         
    
    def createRestartTrajectoryAndIntegrator(self):
        '''initialize system from previous trajectory'''
        # Initialize system state from the restart trajectory
        self.mmtkUniverse.setFromTrajectory(Trajectory(self.mmtkUniverse, self.inventory.restartFilename))
        # Create trajectory and integrator.
        self.mmtkTrajectory = Trajectory(self.mmtkUniverse, self.inventory.trajectoryFilename, "a")
        self.mmtkIntegrator = VelocityVerletIntegrator(self.mmtkUniverse, delta_t=self.inventory.timestep*Units.fs)
        # Periodical actions for equilibration output.
        self.equilibration_actions = [TranslationRemover(0, None, 100),
            RotationRemover(0, None, 100),
            LogOutput(self.inventory.logFilename, ('time', 'energy'), 0, None)
            ]  
        # Periodical actions for trajectory output and text log output.
        self.output_actions = [TranslationRemover(0, None, 100),
            TrajectoryOutput(self.mmtkTrajectory,
            ('configuration', 'energy', 'thermodynamic', 'time', 'auxiliary'), 
            0, None, self.equilibrationSteps()), #this last option makes it so none of the equilibration steps are output, consistent with Gulp
            # Write restart data every time step.
            RestartTrajectoryOutput(self.inventory.restartFilename, 1),
            LogOutput(self.inventory.logFilename, ('time', 'energy'), 0, None) 
            ]  
    
    def _integrateNVE(self):
        # Do some equilibration steps
        self.mmtkIntegrator(steps = self.equilibrationSteps(), actions = self.equilibration_actions)
        # Do some "production" steps.
        self.mmtkIntegrator(steps = self.productionSteps(), actions = self.output_actions)
        # Close the trajectory.
        self.mmtkTrajectory.close()
        
    def _integrateNVT(self):
        # Add thermostat 
        self.mmtkUniverse.thermostat = NoseThermostat(self.inventory.sample.i.temperature)
        # Do some equilibration steps and rescaling velocities.
        self.mmtkIntegrator(steps = self.equilibrationSteps(), actions = [VelocityScaler(self.inventory.sample.i.temperature, 
            0.1*self.inventory.sample.i.temperature, 0, None, 100)] + self.equilibration_actions)
        # Do some "production" steps.
        self.mmtkIntegrator(steps = self.productionSteps(),
                       actions = self.output_actions)
        # Close the trajectory.
        self.mmtkTrajectory.close()   
        
    def _integrateNPT(self):
        # Add thermostat and barostat.
        self.mmtkUniverse.thermostat = NoseThermostat(self.inventory.sample.i.temperature)
        self.mmtkUniverse.barostat = AndersenBarostat(self.inventory.sample.i.pressure)
        # Do some equilibration steps, rescaling velocities and resetting the
        # barostat in regular intervals.
        self.mmtkIntegrator(steps = self.equilibrationSteps(),
            actions = [VelocityScaler(self.inventory.sample.i.temperature, 
            0.1*self.inventory.sample.i.temperature, 0, None, 100),
            BarostatReset(100)] + self.equilibration_actions)
        # Do some "production" steps.
        self.mmtkIntegrator(steps = self.productionSteps(),
                       actions = self.output_actions)
        # Close the trajectory.
        self.mmtkTrajectory.close()
        
    def integrate(self):
        '''integrates an atomic system forward in time and produces a trajectory'''
        self.printWarnings()
        self._setForcefield()
        self._setInitialConditions()
        self.createTrajectoryAndIntegrator()
        if self.inventory.ensemble=='nvt':
            self._integrateNVT()
        elif self.inventory.ensemble=='npt':
            self._integrateNPT()
        elif self.inventory.ensemble=='nve':
            self._integrateNVE()
        else:
            raise Exception, 'your ensemble is not suppported by mmtk'
        return

    def restartIntegrate(self):
        '''performs a restart of an md run'''
        self.printWarnings()
        self._setForcefield()
        self._setInitialConditions()
        self.createRestartTrajectoryAndIntegrator()
        if self.inventory.ensemble=='nvt':
            self._integrateNVT()
        elif self.inventory.ensemble=='npt':
            self._integrateNPT()
        elif self.inventory.ensemble=='nve':
            self._integrateNVE()
        else:
            raise Exception, 'your ensemble is not suppported by mmtk'
        
    def execute(self):
        '''writes out the files, starts the executable, and parses the output files'''
        self.printWarnings()
        if self.inventory.runType=='md':
            self.integrate()
        elif self.inventory.runType=='restart md':
            self.restartIntegrate()

    def printWarnings(self):
        if self.inventory.sampleFrequency > self.inventory.timeStep:
            print '''Mmtk does not allow a different sample frequency than every timestep.
            Write frequency will be set to every timestep.''' 
        if self.inventory.dumpFrequency > self.inventory.timeStep:
            print '''Mmtk does not allow a different dump frequency than every timestep.
            Dump frequency will be set to every timestep.'''
            
    def equilibrationSteps(self):
        '''Number of time steps to reach equilibration'''
        if self.inventory.timeStep==0:
            raise Exception, 'please set the time step to a nonzero value'
        else:
            val=int(self.inventory.equilibrationTime/self.inventory.timeStep)
        return val
    
    def productionSteps(self):
        '''Number of time steps to finish production'''
        if self.inventory.timeStep==0:
            raise Exception, 'please set the time step to a nonzero value'
        else:
            return int(self.inventory.productionTime/self.inventory.timeStep)

# main
if __name__ == '__main__':
    pass
  
# version
__id__ = "$Id$"
 
# End of file