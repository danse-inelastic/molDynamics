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
from memd2.MolDynamics import MolDynamics
#from molDynamics.gulp.Coordinates import Coordinates
from os import system, linesep
from memd2.gulp.GulpForcefield import GulpForcefield
from memd2.gulp.OptionWriter import OptionWriter
from memd2.gulp.KeywordWriter import KeywordWriter

class Gulp(MolDynamics):
    """GULP engine for MolDynamics interface.  
    This class maps the DANSE data structures to GULP's input deck.
    """

    import pd
    computeMaterialProperties = pd.bool(default = False)
    computeMaterialProperties.meta['tip'] = 'whether to print material properties'
    
    engineExecutablePath = pd.str()
    engineExecutablePath.meta['tip'] = '''path to the engine's executable'''
    engineExecutablePath.meta['label'] = 'Engine Executable Path'
    
    inputFileName = pd.str(default = 'gulp.gin')
    inputFileName.meta['tip'] = '''input file for executable'''
    
    runType = pd.str(default = 'md')
    #runType.meta['known_plugins'] = ['md', 'optimize', 'fit', 'phonon'] 
    runType.meta['tip'] = 'type of run'
    #runType.meta['importance'] = 9
    
    forcefield = pd.ref(table = GulpForcefield)
    forcefield.meta['tip'] = 'overall types of potentials to use'
  
    def __init__(self, name='gulp'):
        #define visitors
        self.optionWriter = OptionWriter(self.i.sample)
        self.keywordWriter = KeywordWriter()
        if self.runType is 'md':
            from memd2.gulp.Md import Md
            self.runTypeModule = Md()
        elif self.runType is 'optimize':
            from memd2.gulp.Optimize import Optimize
            self.runTypeModule = Optimize()
    
    def listToString(self,list):
        '''give the keyword string representation of the keyword list'''
        st=''
        for i in list:
            st+=i+' '
        return st
        
    def identifyKeywords(self, visitor):
        keywords=[]
        keywords+=visitor.writeGeneralKeywords(self)
        keywords+=self.runTypeModule.identifyKeywords(visitor)
        keywords+=self.potential.identifyKeywords(visitor)
        return keywords
        
    def identifyOptions(self, visitor):
        options=''
        options+=visitor.writeGeneralOptions(self)
        options+=self.runTypeModule.identifyOptions(visitor)
        #options+=self.i.potential.identifyOptions(visitor)
        return options
        
    def execute(self):
        '''writes out the files, starts the executable, and parses the output files'''
        if self.runTypeModule.runTypeIdentifier!='mdRestart':
            self.inputFileContents = \
            self.listToString(self.identifyKeywords(self.keywordWriter))+linesep+\
            self.identifyOptions(self.optionWriter)
            f=file(self.inputFileName,'w')
            f.write(self.inputFileContents)
            f.close()
            system(self.engineExecutablePath+' < '+self.inputDeckName+' > '+self.logFilename)
        else:
            system(self.engineExecutablePath+' < '+self.restartFilename+' >> '+self.logFilename)    
        #parse the files
        #o=OutputParser(self.i.logFilename, self.i)


  
# version
__id__ = "$Id$"
 
# End of file