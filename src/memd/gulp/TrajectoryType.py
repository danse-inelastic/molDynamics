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


class TrajectoryType(Component):


    class Inventory(Component.Inventory):
        import pyre.inventory as pinv
        xyz = pinv.str('*.xyz (Gulp)', default = None)
        


    def __init__(self, name):
        if name is None:
            name = 'facility'

        Component.__init__(self, name, facility='facility')

        return


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

# Generated automatically by PythonMill on Tue Jun 12 21:10:16 2007

# End of file 
