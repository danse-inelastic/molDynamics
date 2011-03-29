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
from pyregui.inventory.extensions.OutputDir import OutputDir
from pyregui.inventory.extensions.InputFile import InputFile

class GeneralSettings(Component):
    '''contains general settings for an application driver'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        engineExecutablePath = InputFile('Engine Executable Path', default = ".")
        engineExecutablePath.meta['tip'] = '''path to the engine's executable'''
        outputDir = OutputDir( 'outputDir', default = "." )
        outputDir.meta['tip'] = 'Output directory'
#        fireballBasisSetPath = inv.str('Fireball Basis Set Path', default = None)
#        fireballBasisSetPath.meta['tip'] = 'directory containing Fdata'

    def __init__(self, name='GeneralSettings'):
        Component.__init__(self, name, facility='facility')

    def _defaults(self):
        Component._defaults(self)

    def _configure(self):
        Component._configure(self)

    def _init(self):
        Component._init(self)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Sun Jun 24 21:57:30 2007

# End of file 
