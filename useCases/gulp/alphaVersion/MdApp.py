#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#from memd.gulp.Gulp import Gulp
#from memd.mmtk.Mmtk import Mmtk
#from memd.MolDynamics import MolDynamics
from pyre.applications.Script import Script

class MdApp(Script):
    '''Driver for the md engines in DANSE.'''
    class Inventory(Script.Inventory):
        import pyre.inventory as pinv 
        mdEngine = pinv.facility('Molecular Dynamics Engine', default='gulp')
        mdEngine.meta['tip'] = 'which md engine to use'
        mdEngine.meta['known_plugins'] = ['gulp','mmtk']
        #mdEngine.validator=pinv.choice([Gulp(),Mmtk()])

    def __init__(self):
        Script.__init__(self, 'MdApp')
        self.i=self.inventory
        
    def main(self, *args, **kwds):
        self.i.mdEngine.execute()


def main():
    app = MdApp( )
    app.run()
    return

if __name__ == "__main__": #main()
    app = MdApp( )
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
