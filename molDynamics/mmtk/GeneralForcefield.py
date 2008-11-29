#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.components.Component import Component 

class GeneralForcefield(Component):
    '''Represents the Amber set of potential options from MMTK'''
    
    class Inventory(Component.Inventory):
        pass


    def __init__(self, name='GeneralForcefield'):
        Component.__init__(self, name, facility='facility')
        self.i=self.inventory

    def getForcefield(self):
        '''returns the correct mmtk forcefield object'''
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
        
    def _defaults(self):
        Component._defaults(self)
        return

    def _configure(self):
        Component._configure(self)
        return

    def _init(self):
        Component._init(self)
        return


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Wed Jun 13 15:20:21 2007

# End of file 
