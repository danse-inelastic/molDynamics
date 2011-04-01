
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
