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
from molDynamics.MolDynamics import MolDynamics
#from molDynamics.gulp.Coordinates import Coordinates
from os import system, linesep
from molDynamics.gulp.Potential import Potential
from molDynamics.gulp.OptionWriter import OptionWriter
from molDynamics.gulp.KeywordWriter import KeywordWriter


class Gulp(MolDynamics):
    """GULP MD engine for MolDynamics interface.  
This class maps the DANSE data structures to GULP's input deck.
"""

    class Inventory(MolDynamics.Inventory):
        import pyre.inventory as inv
        computeMaterialProperties = inv.bool('Compute Material Properties', default = False)
        computeMaterialProperties.meta['tip'] = 'whether to print material properties'
        inputDeckName = inv.str('Input Filename', default = 'molDynamics.gin')
        inputDeckName.meta['tip'] = '''input file for executable'''
        runType = inv.facility('runType', default = 'md')
        runType.meta['known_plugins'] = ['md', 'optimize', 'fit', 'phonon'] 
        runType.meta['tip'] = 'type of run'
        runType.meta['importance'] = 9
        potential = inv.facility('Potential', default = Potential())
        potential.meta['tip'] = 'overall types of potentials to use'
  
    def __init__(self, name='gulp'):
        MolDynamics.__init__(self, name, 'mdEngine')
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
        '''writes out the files and starts the executable'''
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

  
# version
__id__ = "$Id$"
 
# End of file