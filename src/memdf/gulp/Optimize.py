from memdf.gulp.Gulp import Gulp
class Optimize(Gulp):
    '''This class serves as an API/interface for md engines.'''
    constraints = 'None'
    #['None', 'constant_volume', 'constant_pressure'
    optimizeCell = False
    optimizeCoordinates = False
    trajectoryFilename = 'molDynamics'
    restartFilename = 'molDynamics.res'
                        
    def __init__(self, **kwds):
        Gulp.__init__(self, **kwds)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        self.runTypeIdentifier='optimize'
        
    def identifySettings(self, visitor):     
        return visitor.writeOptimizeSettings(self)
    
    def writeKeywords(self, visitor): 
        keywords=[]
        keywords+=visitor.writeOptimizeKeywords(self)
        keywords+=visitor.writeGulpKeywords(self)
        return keywords
    
    def writeOptions(self, visitor):
        options=''
        options+=visitor.writeGulpOptions(self)
        options+=visitor.writeOptimizeOptions(self)
        return options
