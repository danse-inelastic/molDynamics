from memd.gulp.Visitable import Visitable

class Optimize(Visitable):
    '''This class serves as an API/interface for md engines.'''
    constraints = 'None'
    #['None', 'constant_volume', 'constant_pressure'
    optimizeCell = False
    optimizeCoordinates = False
    trajectoryFilename = 'molDynamics'
    restartFilename = 'molDynamics.res'
                        
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        self.runTypeIdentifier='optimize'
        
    def identifySettings(self, visitor): 
        return visitor.writeOptimizeSettings(self)
    
    def identifyKeywords(self, visitor): 
        return visitor.writeOptimizeKeywords(self)
    
    def identifyOptions(self, visitor): 
        return visitor.writeOptimizeOptions(self)
