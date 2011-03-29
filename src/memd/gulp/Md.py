from memd.gulp.Gulp import Gulp
class Md(Gulp):
    '''This class serves as an md property setter.'''
    
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

#    trajectoryType = inv.str('trajectoryType', default='xyz')
#    trajectoryType.meta['tip'] = 'type of trajectory output'  
#    trajectoryType.validator=inv.choice(['xyz', 'history', 'xyz and history'])
                        
    def __init__(self, **kwds):
        Gulp.__init__(self, **kwds)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
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
    
    def writeKeywords(self, visitor): 
        keywords=[]
        keywords+=visitor.writeMdKeywords(self)
        keywords+=visitor.writeGulpKeywords(self)
        return keywords
    
    def writeOptions(self, visitor):
        options=''
        options+=visitor.writeGulpOptions(self)
        options+=visitor.writeMdOptions(self)
        return options
