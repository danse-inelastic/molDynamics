
#from memdf.gulp.forcefields.InputFile import InputFile

class Potential(object):
    '''This class serves as an API/interface for gulp potential construction.'''
    # 
    dispersionInRecipSpace = False
    useInitialBondingOnly = False
    forcefield = ''
    moleculeIdentification = 'None'
    #['None','identify molecules; remove intramolecular Coulomb forces',
    #                                             'identify molecules; retain intramolecular Coulomb forces'])
      
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  

    def identifyOptions( self, visitor): 
        return visitor.writePotentialOptions(self)
    
    def identifyKeywords( self, visitor): 
        return visitor.writePotentialKeywords(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 