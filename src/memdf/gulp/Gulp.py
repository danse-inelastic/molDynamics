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
#
from memdf.MolDynamics import MolDynamics
#from memd.gulp.Coordinates import Coordinates
from os import system, linesep
#from Potential import Potential
from OptionWriter import OptionWriter
from KeywordWriter import KeywordWriter

class Gulp(MolDynamics):
    """GULP engine for MolDynamics interface.  
    This class maps the DANSE data structures to GULP's input deck.
    """
    computeMaterialProperties = False
    engineExecutablePath=''
    inputDeckName='memd.gin'
    #runType = 'md'
    #['md', 'optimize', 'fit', 'phonon']
    #potential = Potential()
    dispersionInRecipSpace = False
    useInitialBondingOnly = False
    forcefield = ''
    moleculeIdentification = 'None'
    
    def __init__(self, **kwds):
        MolDynamics.__init__(self)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        #define visitors
        self.optionWriter = OptionWriter()
        self.keywordWriter = KeywordWriter()
  
    def listToString(self,list):
        '''give the keyword string representation of the keyword list'''
        st=''
        for i in list:
            st+=i+' '
        return st

    def writeInputfile(self):
        self.inputFileContents = \
        self.listToString(self.writeKeywords(self.keywordWriter))+linesep+\
        self.writeOptions(self.optionWriter)
        f=file(self.inputDeckName,'w')
        f.write(self.inputFileContents)
        f.close()
        
    def execute(self):
        '''writes out the files, starts the executable, and parses the output files'''
        if self.runType.runTypeIdentifier!='mdRestart':
            self.writeInputfile()
            system(self.engineExecutablePath+' < '+self.inputDeckName+' > '+self.logFilename)
        else:
            system(self.engineExecutablePath+' < '+self.restartFilename+' >> '+self.logFilename)    
        #parse the files
        #o=OutputParser(self.logFilename, self.i)


  
# version
__id__ = "$Id$"
 
# End of file