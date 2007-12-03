#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.applications.Script import Script
#from molDynamics.mmtk.Mmtk import Mmtk
#from molDynamics.gulp.Gulp import Gulp

class MdApp(Script):
    '''Driver for the md engines in DANSE.'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        mdEngine = inv.facility('mdEngine', default='gulp')
        mdEngine.meta['known_plugins'] = ['gulp','mmtk']
        #mdEngine = inv.facility('Molecular Dynamics Engine', default=Gulp())
        #mdEngine = inv.facility('Molecular Dynamics Engine', default=Mmtk())
        mdEngine.meta['tip'] = 'which md engine to use'

    def __init__(self):
        Script.__init__(self, 'MdApp')
        self.i=self.inventory
        
    def main(self, *args, **kwds):
        self.i.mdEngine.execute()

if __name__=='__main__':
    app=MdApp()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
