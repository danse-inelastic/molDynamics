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
from sample.Sample import Sample
from pyre.components.Component import Component
from pyregui.inventory.extensions.OutputDir import OutputDir


class MolDynamics(Component):
    '''This class serves as an API/interface for md engines.'''
    
    class Inventory(Component.Inventory):
        import pyre.inventory as inv  
        sample = inv.facility('Sample',default = Sample())
        sample.meta['importance'] = 10
        sample.meta['tip'] = 'piece of material being measured/simulated'

        logFilename = inv.str('Log Filename', default = 'molDynamics.log')
        logFilename.meta['tip'] = 'name of log file for md run'

        
        outputDir = OutputDir( 'outputDir', default = "" )
        outputDir.meta['tip'] = 'Output directory'

#        restartFilename = inv.str('Restart Filename', default = 'molDynamics.res')
#        restartFilename.meta['tip'] = '''restart file for md executable'''

                        
    def __init__(self, name='MolDynamics', facility=None):
        Component.__init__(self, name, facility)
        self.i=self.inventory
    
#    def _configure(self):
#        Component._configure(self)
#        #self.sample = self.i.sample


    def execute(self):
        ''' subclasses (engines) must implement this class and parse appropriate 
output files to get data as dataobjects which can be returned below'''
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 