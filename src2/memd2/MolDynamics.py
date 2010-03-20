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

class MolDynamics:
    '''This class serves as an API/interface for md engines.'''
    
    import pd 
    matter = pd.ref()
    matter.meta['importance'] = 10
    matter.meta['tip'] = 'piece of material being measured/simulated'

    logFilename = pd.str()
    logFilename.meta['tip'] = 'name of log file'

    outputDir = pd.str()
    outputDir.meta['tip'] = 'output directory'

#        restartFilename = inv.str('Restart Filename', default = 'molDynamics.res')
#        restartFilename.meta['tip'] = '''restart file for md executable''

    def execute(self):
        ''' subclasses (engines) must implement this class and parse appropriate 
output files to get data as dataobjects which can be returned below'''
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)


# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 