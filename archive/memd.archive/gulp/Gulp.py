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
from memd.MolDynamics import MolDynamics
#from memd.gulp.Coordinates import Coordinates
from os import system, linesep
from memd.gulp.Potential import Potential
from memd.gulp.OptionWriter import OptionWriter
from memd.gulp.KeywordWriter import KeywordWriter
#from pyregui.inventory.extensions.InputFile import InputFile

class Gulp(MolDynamics):
    """GULP MD engine for MolDynamics interface.  
    This class maps the DANSE data structures to GULP's input deck.
    """

    class Inventory(MolDynamics.Inventory):
        import pyre.inventory as inv
        computeMaterialProperties = inv.bool('computeMaterialProperties', default = False)
        computeMaterialProperties.meta['tip'] = 'whether to print material properties'
        
        engineExecutablePath = inv.str('engineExecutablePath', default = "")
        engineExecutablePath.meta['tip'] = '''path to the engine's executable'''
        
        inputDeckName = inv.str('inputDeckName', default = 'memd.gin')
        inputDeckName.meta['tip'] = '''input file for executable'''
        
        runType = inv.facility('runType', default = 'md')
        runType.meta['known_plugins'] = ['md', 'optimize', 'fit', 'phonon'] 
        runType.meta['tip'] = 'type of run'
        runType.meta['importance'] = 9
        
        potential = inv.facility('potential', default = Potential())
        potential.meta['tip'] = 'overall types of potentials to use'
  
    def __init__(self, name='gulp'):
        MolDynamics.__init__(self, name, 'engine')
        self.i = self.inventory
        #define visitors
        self.optionWriter = OptionWriter(self.i.sample)
        self.keywordWriter = KeywordWriter()
    
    def _configure(self):
        MolDynamics._configure(self)
    
    def listToString(self,list):
        '''give the keyword string representation of the keyword list'''
        st=''
        for i in list:
            st+=i+' '
        return st
        
    def identifyKeywords(self, visitor):
        keywords=[]
        keywords+=visitor.writeGeneralKeywords(self)
        keywords+=self.i.runType.identifyKeywords(visitor)
        keywords+=self.i.potential.identifyKeywords(visitor)
        return keywords
        
    def identifyOptions(self, visitor):
        options=''
        options+=visitor.writeGeneralOptions(self)
        options+=self.i.runType.identifyOptions(visitor)
        #options+=self.i.potential.identifyOptions(visitor)
        return options
        
    def execute(self):
        '''writes out the files, starts the executable, and parses the output files'''
        if self.i.runType.runTypeIdentifier!='mdRestart':
            self.inputFileContents = \
            self.listToString(self.identifyKeywords(self.keywordWriter))+linesep+\
            self.identifyOptions(self.optionWriter)
            f=file(self.i.inputDeckName,'w')
            f.write(self.inputFileContents)
            f.close()
            system(self.i.engineExecutablePath+' < '+self.i.inputDeckName+' > '+self.i.logFilename)
        else:
            system(self.i.engineExecutablePath+' < '+self.i.restartFilename+' >> '+self.i.logFilename)    
        #parse the files
        #o=OutputParser(self.i.logFilename, self.i)


  
# version
__id__ = "$Id$"
 
# End of file