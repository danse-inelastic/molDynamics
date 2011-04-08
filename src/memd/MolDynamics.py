
#from Sample import Sample
class MolDynamics(object):
    '''This class serves as an API/interface for md engines.'''
    
    #sample = Sample()
    xyzFile=''
    logFilename = 'molDynamics.log'
    outputDir = ''
                        
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  

    def initializeFromFile(self):
        try:
            f=file(self.xyzFile)
        except:
            print "cannot open xyz file"
            raise
        self.atomStrings = f.readlines()
        try:
            ax,ay,az,bx,by,bz,cx,cy,cz = self.atomStrings[1].split()
            self.ucVecs = [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]
        except:
            ax,ay,az,bx,by,bz,cx,cy,cz = 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0
            self.ucVecs = [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]
        return ax,ay,az,bx,by,bz,cx,cy,cz
    
    def getAtomsAsStrings(self):
        if not hasattr(self, 'atomStrings'):
            self.initializeFromFile()
        return self.atomStrings[2:]
    
    def getCellVectors(self):
        if not hasattr(self, 'ucVecs'):
            self.initializeFromFile()
        return self.ucVecs