#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2007 All Rights Reserved  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from mdt.Gulp import Gulp

class GulpPhonon(Gulp):
    '''Gulp phonon calculation'''
    
    kpoint_mesh = [0, 0, 0]
    dosdispersionfile = "gulp.phonons"
    broaden_dos = False
    project_dos = ''
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        super(GulpPhonon, self).__init__()
        
        
