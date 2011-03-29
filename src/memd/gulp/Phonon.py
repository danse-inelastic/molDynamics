from memd.gulp.Gulp import Gulp
class Phonon(Gulp):
    '''This class allows phonon calculations using traditional molecular mechanics potentials.'''
    
    kpointMesh = ''
    dosAndDispersionFilename = ""
    broadenDos = False
    projectDos = ''
                        
    def __init__(self, **kwds):
        Gulp.__init__(self, **kwds)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        self.runTypeIdentifier='phonon'
    
    def writeKeywords(self, visitor): 
        keywords=[]
        keywords+=visitor.writePhononKeywords(self)
        keywords+=visitor.writeGulpKeywords(self)
        return keywords
    
    def writeOptions(self, visitor):
        options=''
        gopts = visitor.writeGulpOptions(self)
        options+=gopts
        options+=visitor.writePhononOptions(self)
        return options
    
    def identifySettings( self, visitor): 
        return visitor.writePhononSettings(self)
