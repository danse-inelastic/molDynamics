#!/usr/bin/env python
from memd.MolDynamics import MolDynamics
import math
import MMTK
from MMTK import Units
from MMTK.ForceFields import LennardJonesForceField, Amber94ForceField, Amber99ForceField
from MMTK.Environment import NoseThermostat, AndersenBarostat
from MMTK.Trajectory import Trajectory, TrajectoryOutput, LogOutput, RestartTrajectoryOutput
from MMTK.Dynamics import VelocityVerletIntegrator, VelocityScaler, \
                          TranslationRemover, RotationRemover,BarostatReset
from MMTK.ForceFields import LennardJonesForceField as LennardJonesFF
import numpy as np
  
class Mmtk(MolDynamics):
    """MMTK engine for MolDynamics interface.
    
    This class maps the API to MMTK commands and executes them.
    """
    ensemble = 'nvt'
    equilibrationTime = 0.0
    productionTime = 0.0
    propCalcInterval = 5.0
    thermostatParameter = 0.05
    barostatParameter = 0.0
    timeStep = 0.002
    trajectoryFilename = 'molDynamics.his'
    restartFilename = 'molDynamics.res'
    dumpInterval = 0.0
    temperature=0.0
    pressure=0.0
    integrator = 'velocity-verlet'
    restarting = False
    forcefield = 'amber'
    ljCutoff = 15.*Units.Ang
    #'amber', 'lennardJones']
        
    def __init__(self, **kwds):
        MolDynamics.__init__(self, **kwds)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        self.mmtkUniverse = None
        
#    def _setDefaults(self):
#        '''set defaults specific to mmtk'''
#        self.trajectoryFilename = 'molDynamics.nc'
#        self.restartFilename = 'restart.nc'
#        self.propCalcInterval = self.timeStep*Units.fs
#        self.dumpInterval = self.timeStep*Units.fs
        
    def _ind(self,list):
        """gives the indices of the list to iterate over"""
        return range(len(list))
    
    def appEqual(self,v1,v2):
        '''equal to within a certain numerical accuracy'''
        if v1-v2<10**-6:
            return True
        else:
            return False
        
    def _setForcefield(self):         
        if self.forcefield=='amber94':
            self.ff=Amber94ForceField()
        elif self.forcefield=='lennard jones':
            self.ff=LennardJonesFF(eval(self.ljCutoff))
        else: #'amber99'
            self.ff=Amber99ForceField()
        
    def _setInitialConditions(self):
        '''map MolDynamics unit cell stuff to MMTK's. 
        Eventually much of this will be taken by the crystal class''' 
        #atoms = self.getAtomsAsStrings()
        #uc = self.getCellVectors()
        uc=self.structure.lattice.base
        if uc.all()==np.array([[1.0, 0, 0],[0, 1.0, 0.0],[0.0, 0.0, 1.0]]).all():
            self.mmtkUniverse = MMTK.InfiniteUniverse(self.ff)
        else:
            #ucList=uc.tolist()
            a,b,c,al,be,ga = uc.abcABG()
            if self.appEqual(al, 90.0) and self.appEqual(be, 90.0) and self.appEqual(ga, 90.0):
                if a==b and b==c:
                    self.mmtkUniverse = MMTK.CubicPeriodicUniverse(a*Units.Ang, self.ff)
                else:
                    self.mmtkUniverse = MMTK.OrthorhombicPeriodicUniverse(
                            (a*Units.Ang, b*Units.Ang, c*Units.Ang), self.ff)
            else:
                uc = self.sample.unitCell
                self.mmtkUniverse = MMTK.ParallelepipedicPeriodicUniverse(
                    ((uc[0][0]*Units.Ang, uc[0][1]*Units.Ang, uc[0][2]*Units.Ang),
                     (uc[1][0]*Units.Ang, uc[1][1]*Units.Ang, uc[1][2]*Units.Ang),
                     (uc[2][0]*Units.Ang, uc[2][1]*Units.Ang, uc[2][2]*Units.Ang)), self.ff)
        #add objects to mmtkUniverse
        for atom in self.structure:
            x, y, z = atom.xyz_cartn
            self.mmtkUniverse.addObject(MMTK.Atom(atom.symbol, position = \
                MMTK.Vector(x*Units.Ang, y*Units.Ang, z*Units.Ang))) 
#        elif self.sample.has_attribute('molecule'):
#            pass
        
    def createTrajectoryAndIntegrator(self):
        '''create trajectory and integrator'''
        #initialize velocities--this has to happen after adding atoms
        self.mmtkUniverse.initializeVelocitiesToTemperature(self.temperature)
        # Create trajectory and integrator.
        self.mmtkTrajectory = Trajectory(self.mmtkUniverse, self.trajectoryFilename, "w")
        self.mmtkIntegrator = VelocityVerletIntegrator(self.mmtkUniverse, delta_t=self.timeStep*Units.fs)
        # Periodical actions for equilibration output.
        self.equilibration_actions = [TranslationRemover(0, None, 100),
            RotationRemover(0, None, 100),
            LogOutput(self.logFilename, ('time', 'energy'), 0, None)
            ]  
        # Periodical actions for trajectory output and text log output.
        self.output_actions = [TrajectoryOutput(self.mmtkTrajectory,
            ('configuration', 'energy', 'thermodynamic', 'time', 'auxiliary'), 
            0, None, 20), #TODO: Fixme so the user can specify when trajectory and sample frequency happens
            #this last option makes it so none of the equilibration steps are output, consistent with Gulp
            LogOutput(self.logFilename, ('time', 'energy'), 0, None, 20) #this last 0 makes it so all equilibration steps are output, consistent with Gulp
            ]         
    
    def createRestartTrajectoryAndIntegrator(self):
        '''initialize system from previous trajectory'''
        # Initialize system state from the restart trajectory
        self.mmtkUniverse.setFromTrajectory(Trajectory(self.mmtkUniverse, self.restartFilename))
        # Create trajectory and integrator.
        self.mmtkTrajectory = Trajectory(self.mmtkUniverse, self.trajectoryFilename, "a")
        self.mmtkIntegrator = VelocityVerletIntegrator(self.mmtkUniverse, delta_t=self.timestep*Units.fs)
        # Periodical actions for equilibration output.
        self.equilibration_actions = [TranslationRemover(0, None, 100),
            RotationRemover(0, None, 100),
            LogOutput(self.logFilename, ('time', 'energy'), 0, None)
            ]  
        # Periodical actions for trajectory output and text log output.
        self.output_actions = [TranslationRemover(0, None, 100),
            TrajectoryOutput(self.mmtkTrajectory,
            ('configuration', 'energy', 'thermodynamic', 'time', 'auxiliary'), 
            0, None, self.equilibrationSteps()), #this last option makes it so none of the equilibration steps are output, consistent with Gulp
            # Write restart data every time step.
            RestartTrajectoryOutput(self.restartFilename, 1),
            LogOutput(self.logFilename, ('time', 'energy'), 0, None) 
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
        self.mmtkUniverse.thermostat = NoseThermostat(self.temperature)
        # Do some equilibration steps and rescaling velocities.
        self.mmtkIntegrator(steps = self.equilibrationSteps(), actions = [VelocityScaler(self.temperature, 
            0.1*self.temperature, 0, None, 100)] + self.equilibration_actions)
        # Do some "production" steps.
        self.mmtkIntegrator(steps = self.productionSteps(),
                       actions = self.output_actions)
        # Close the trajectory.
        self.mmtkTrajectory.close()   
        
    def _integrateNPT(self):
        # Add thermostat and barostat.
        self.mmtkUniverse.thermostat = NoseThermostat(self.temperature)
        self.mmtkUniverse.barostat = AndersenBarostat(self.pressure)
        # Do some equilibration steps, rescaling velocities and resetting the
        # barostat in regular intervals.
        self.mmtkIntegrator(steps = self.equilibrationSteps(),
            actions = [VelocityScaler(self.temperature, 
            0.1*self.temperature, 0, None, 100),
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
        if self.ensemble=='nvt':
            self._integrateNVT()
        elif self.ensemble=='npt':
            self._integrateNPT()
        elif self.ensemble=='nve':
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
        if self.ensemble=='nvt':
            self._integrateNVT()
        elif self.ensemble=='npt':
            self._integrateNPT()
        elif self.ensemble=='nve':
            self._integrateNVE()
        else:
            raise Exception, 'your ensemble is not suppported by mmtk'
        
    def execute(self):
        '''writes out the files, starts the executable, and parses the output files'''
        self.printWarnings()
        if self.restarting:
            self.restartIntegrate()
        else:
            self.integrate()
            
    def printWarnings(self):
        if self.propCalcInterval > self.timeStep:
            print '''Mmtk does not allow a different sample frequency than every timestep.
            Write frequency will be set to every timestep.''' 
        if self.dumpInterval > self.timeStep:
            print '''Mmtk does not allow a different dump frequency than every timestep.
            Dump frequency will be set to every timestep.'''
            
    def equilibrationSteps(self):
        '''Number of time steps to reach equilibration'''
        if self.timeStep==0:
            raise Exception, 'please set the time step to a nonzero value'
        else:
            val=int(self.equilibrationTime/self.timeStep)
        return val
    
    def productionSteps(self):
        '''Number of time steps to finish production'''
        if self.timeStep==0:
            raise Exception, 'please set the time step to a nonzero value'
        else:
            return int(self.productionTime/self.timeStep)

# main
if __name__ == '__main__':
    pass
  
# version
__id__ = "$Id$"
 
# End of file