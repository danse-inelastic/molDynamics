#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Brandon Keith
#                      California Institute of Technology
#              (C) 2009 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.applications.Script import Script

class MdApp(Script):
    '''Driver for the md engines in DANSE.'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        engine = inv.facility('engine', default='gulp')
        engine.meta['known_plugins'] = ['gulp','mmtk']
        engine.meta['tip'] = 'which md engine to use'

    def __init__(self):
        Script.__init__(self, 'MdApp')
        self.i = self.inventory
        
    def _configure(self):
        self.engine = self.i.engine
        
    def main(self, *args, **kwds):
        self.engine.execute()

if __name__=='__main__':
    app=MdApp()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
