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
from Sample import Sample

class MolDynamics(object):
    '''This class serves as an API/interface for md engines.'''
    
    sample = Sample()
    logFilename = 'molDynamics.log'
    outputDir = ''
                        
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
            

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Mon Apr 16 12:44:30 2007

# End of file 