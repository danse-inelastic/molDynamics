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
    barostatParameter = pd.float(default = 0.005)
    barostatParameter.meta['tip'] = '''barostat parameter to keep fluctuations relatively small'''
    barostatParameter.meta['label'] = 'Barostat Parameter'
    
    ensemble= pd.str(default = 'nve') 
    #ensemble.validator=pd.choice(["nve", "nvt", "npt"])
    ensemble.meta['tip'] = 'thermodynamic ensemble (nve, nvt, npt, ...)'
    ensemble.meta['label'] = 'Thermodynamic Ensemble'
    
    equilibrationTime = pd.float(default = 0.0)
    equilibrationTime.meta['tip'] = 'equilibration time of the simulation (ps)'
    equilibrationTime.meta['label'] = 'Equilibration Time (ps)'
    
    productionTime = pd.float(default = 5.0)
    productionTime.meta['tip'] = 'production time of the simulation'
    productionTime.meta['label'] = 'Production Time (ps)'
    
    sampleFrequency = pd.float(default = 5.0)
    sampleFrequency.meta['tip'] = '''frequency at which sampled properties are 
written to trajectory and log file'''
    sampleFrequency.meta['label'] = 'Properties Calculation Frequency (fs)'
    
    thermostatParameter = pd.float(default = 0.05)
    thermostatParameter.meta['tip'] = '''thermostat parameter to keep 
fluctuations relatively small'''
    thermostatParameter.meta['label'] = 'Thermostat Parameter'
    
    timeStep = pd.float(default = 0.001)
    timeStep.meta['tip'] = 'integration time step (ps)'
    timeStep.meta['label'] = 'Time step (fs)'
    
    trajectoryFilename = pd.str(default='molDynamics')
    trajectoryFilename.meta['tip'] = 'name of trajectory file(s)'
    trajectoryFilename.meta['label'] = 'Trajectory Filename'

    restartFilename = pd.str('molDynamics.res')
    restartFilename.meta['tip'] = '''restart file for resuming an md run or optimization'''
    restartFilename.meta['label'] = 'Restart Filename'
    
    dumpFrequency = pd.float(default = 0.0)
    dumpFrequency.meta['tip'] = '''frequency at which a restart file is written'''
    dumpFrequency.meta['label'] = 'Dump Frequency (ps)'

    trajectoryType = pd.str(default='xyz')
    trajectoryType.meta['tip'] = 'type of trajectory output'  
    trajectoryType.meta['label'] = 'Trajectory Type'
    
    #trajectoryType.validator = pd.choice(['xyz', 'history', 'xyz and history'])
                        
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