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
from Potential import Potential
from OptionWriter import OptionWriter
from KeywordWriter import KeywordWriter

class Gulp(MolDynamics):
    """GULP MD engine for MolDynamics interface.  
    This class maps the DANSE data structures to GULP's input deck.
    """
    computeMaterialProperties = False
    engineExecutablePath=''
    inputDeckName='memd.gin'
    runType = 'md'
    #['md', 'optimize', 'fit', 'phonon']
    potential = Potential()
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        MolDynamics.__init__(self)
        #define visitors
        self.optionWriter = OptionWriter(self.sample)
        self.keywordWriter = KeywordWriter()
    
    def listToString(self,list):
        '''give the keyword string representation of the keyword list'''
        st=''
        for i in list:
            st+=i+' '
        return st
        
    def identifyKeywords(self, visitor):
        keywords=[]
        keywords+=visitor.writeGeneralKeywords(self)
        keywords+=self.runType.identifyKeywords(visitor)
        keywords+=self.potential.identifyKeywords(visitor)
        return keywords
        
    def identifyOptions(self, visitor):
        options=''
        options+=visitor.writeGeneralOptions(self)
        options+=self.runType.identifyOptions(visitor)
        #options+=self.potential.identifyOptions(visitor)
        return options
        
    def execute(self):
        '''writes out the files, starts the executable, and parses the output files'''
        if self.runType.runTypeIdentifier!='mdRestart':
            self.inputFileContents = \
            self.listToString(self.identifyKeywords(self.keywordWriter))+linesep+\
            self.identifyOptions(self.optionWriter)
            f=file(self.inputDeckName,'w')
            f.write(self.inputFileContents)
            f.close()
            system(self.engineExecutablePath+' < '+self.inputDeckName+' > '+self.logFilename)
        else:
            system(self.engineExecutablePath+' < '+self.restartFilename+' >> '+self.logFilename)    
        #parse the files
        #o=OutputParser(self.logFilename, self.i)


  
# version
__id__ = "$Id$"
 
# End of file