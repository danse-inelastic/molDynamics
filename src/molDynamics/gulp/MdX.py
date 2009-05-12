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
from pyre.components.Component import Component
#from molDynamics.Md import Md as MdBase
from os import linesep
from molDynamics.gulp.Visitable import Visitable


class Md(Component,Visitable):#(MdBase):
    '''This class serves as an md property setter.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
        barostatParameter = inv.float('Barostat Parameter', default = 0.005)
        barostatParameter.meta['tip'] = '''barostat parameter to keep fluctuations relatively small'''
        
        ensemble= inv.str('Thermodynamic Ensemble', default = 'nve') 
        ensemble.validator=inv.choice(["nve", "nvt", "npt"])
        ensemble.meta['tip'] = 'thermodynamic ensemble (nve, nvt, npt, ...)'
        
        equilibrationTime = inv.float('Equilibration Time (ps)', default = 0.1)
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
        restartFilename.meta['tip'] = '''restart file for resuming an md run'''
        
        dumpFrequency = inv.float('Dump Frequency (ps)', default = 0.0)
        dumpFrequency.meta['tip'] = '''frequency at which a restart file is written'''

        trajectoryType = inv.str('Trajectory Type', default='xyz')
        trajectoryType.meta['tip'] = 'type of trajectory output'  
        trajectoryType.validator=inv.choice(['xyz', 'history', 'xyz and history'])
                        
    def __init__(self, name='md'):
        Component.__init__(self, name,'runType')
        self.i=self.inventory
        self.runTypeIdentifier='md'
    
#    def _configure(self):
#        Component._configure(self)
#        #self.sample = self.i.sample
    
    def equilibrationSteps(self):
        '''Number of time steps to reach equilibration'''
        if self.i.timeStep==0:
            raise Exception, 'please set the time step to a nonzero value'
        else:
            val=int(self.i.equilibrationTime/self.i.timeStep)
        return val
    
    def productionSteps(self):
        '''Number of time steps to finish production'''
        if self.i.timeStep==0:
            raise Exception, 'please set the time step to a nonzero value'
        else:
            return int(self.i.productionTime/self.i.timeStep)

    def execute(self):
        ''' subclasses (engines) must implement this class and parse appropriate 
output files to get data as dataobjects which can be returned below'''
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)

    def getFinalConfiguration(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    def getTrajectoryFile(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    def getMaterialProperties(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    def identify( self, visitor): 
        return visitor.writeMdSettings(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 