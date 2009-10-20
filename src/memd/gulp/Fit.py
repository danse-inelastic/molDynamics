#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.components.Component import Component
from molDynamics.gulp.forcefields.InputFile import InputFile


class Fit(Component):
    '''This class fits forcefields to various experimental and ab initio quantities, which for now is mostly ab initio energies.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        constraints = inv.str('Constraints', default = 'None')
        constraints.meta['tip'] = '''constraints on the cell'''
        constraints.validator = inv.choice(['None', 'constant volume', 'constant pressure'])

        energies = inv.facility('Ab initio Energies', default=InputFile('ab initio energies'))
        energies.meta['tip'] = 'a pickled file containing a list of ab initio energies'

        structures = inv.facility('Structures', default=InputFile('ab initio energies'))
        structures.meta['tip'] = 'a pickled file containing a list of ab initio energies'
        
                   
    def __init__(self, name='fit'):
        Component.__init__(self, name, 'runType')
        self.i=self.inventory
        self.runTypeIdentifier='fit'
    
    def identifyOptions( self, visitor): 
        return visitor.writeFitOptions(self)
    
    def identifyKeywords( self, visitor): 
        return visitor.writeFitKeywords(self)
    
#    def _configure(self):
#        Component._configure(self)
#        #self.sample = self.i.sample


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 