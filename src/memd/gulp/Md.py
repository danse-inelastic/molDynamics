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
from memd.gulp.Visitable import Visitable


class Md(Component,Visitable):#(MdBase):
    '''This class serves as an md property setter.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
        barostatParameter = inv.float('barostatParameter', default = 0.005)
        barostatParameter.meta['tip'] = '''barostat parameter to keep fluctuations relatively small'''
        
        ensemble= inv.str('ensemble', default = 'nve') 
        ensemble.validator=inv.choice(["nve", "nvt", "npt"])
        ensemble.meta['tip'] = 'thermodynamic ensemble (nve, nvt, npt, ...)'
        
        equilibrationTime = inv.float('equilibrationTime', default = 0.0)
        equilibrationTime.meta['tip'] = 'equilibration time of the simulation (ps)'
        
        productionTime = inv.float('productionTime', default = 5.0)
        productionTime.meta['tip'] = 'production time of the simulation'
        
        propCalcInterval = inv.float('propCalcInterval', default = 5.0)
        propCalcInterval.meta['tip'] = '''frequency at which sampled properties are 
written to trajectory and log file'''
        
        thermostatParameter = inv.float('thermostatParameter', default = 0.005)
        thermostatParameter.meta['tip'] = '''thermostat parameter to keep 
fluctuations relatively small'''
        
        timeStep = inv.float('timeStep', default = 0.5)
        timeStep.meta['tip'] = 'integration time step (ps)'
        
        trajectoryFilename = inv.str('trajectoryFilename', default='molDynamics')
        trajectoryFilename.meta['tip'] = 'name of trajectory file(s)'

        restartFilename = inv.str('restartFilename', default = 'molDynamics.res')
        restartFilename.meta['tip'] = '''restart file for resuming an md run or optimization'''
        
        dumpInterval = inv.float('dumpInterval', default = 0.0)
        dumpInterval.meta['tip'] = '''interval at which a restart file is written'''

        trajectoryType = inv.str('trajectoryType', default='xyz')
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



# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 