#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#from molDynamics.Md import Md as MdBase
from molDynamics.gulp.Visitable import Visitable

class Md(Visitable):#(MdBase):
    '''This class serves as an md property setter.'''
    
    import pd
    barostatParameter = pd.float(label = 'Barostat Parameter', default = 0.005)
    barostatParameter.meta['tip'] = '''barostat parameter to keep fluctuations relatively small'''
    
    ensemble= pd.str(label = 'Thermodynamic Ensemble', default = 'nve') 
    ensemble.validator=pd.choice(["nve", "nvt", "npt"])
    ensemble.meta['tip'] = 'thermodynamic ensemble (nve, nvt, npt, ...)'
    
    equilibrationTime = pd.float(label = 'Equilibration Time (ps)', default = 0.0)
    equilibrationTime.meta['tip'] = 'equilibration time of the simulation (ps)'
    
    productionTime = pd.float(label = 'Production Time (ps)', default = 5.0)
    productionTime.meta['tip'] = 'production time of the simulation'
    
    sampleFrequency = pd.float(label = 'Properties Calculation Frequency (fs)', default = 5.0)
    sampleFrequency.meta['tip'] = '''frequency at which sampled properties are 
written to trajectory and log file'''
    
    thermostatParameter = pd.float(label = 'Thermostat Parameter', default = 0.05)
    thermostatParameter.meta['tip'] = '''thermostat parameter to keep 
fluctuations relatively small'''
    
    timeStep = pd.float(label = 'Time step (fs)', default = 0.001)
    timeStep.meta['tip'] = 'integration time step (ps)'
    
    trajectoryFilename = pd.str(label = 'Trajectory Filename', default='molDynamics')
    trajectoryFilename.meta['tip'] = 'name of trajectory file(s)'

    restartFilename = pd.str(label = 'Restart Filename', default = 'molDynamics.res')
    restartFilename.meta['tip'] = '''restart file for resuming an md run or optimization'''
    
    dumpFrequency = pd.float(label = 'Dump Frequency (ps)', default = 0.0)
    dumpFrequency.meta['tip'] = '''frequency at which a restart file is written'''

    trajectoryType = pd.str(label = 'Trajectory Type', default='xyz')
    trajectoryType.meta['tip'] = 'type of trajectory output'  
    trajectoryType.validator = pd.choice(['xyz', 'history', 'xyz and history'])
                        
    def __init__(self, name='md'):
        self.runTypeIdentifier='md'
    
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

    def getFinalConfiguration(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    def getTrajectoryFile(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    def getMaterialProperties(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    def identifyOptions( self, visitor): 
        return visitor.writeMdOptions(self)
    
    def identifyKeywords( self, visitor): 
        return visitor.writeMdKeywords(self)



# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 