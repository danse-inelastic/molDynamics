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

class GulpPhonons(Gulp):
    '''Gulp phonon calculation'''
    
    optimize_coordinates = True
    optimize_cell = False
    constraint = 'constant volume'
    trajectoryfile = 'gulp.his'
    restartfile = 'gulp.res'
    
    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)
        super(GulpPhonons, self).__init__()
        
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']    
try:
    class Inventory(Gulp.Inventory):
        kpoint_mesh = Gulp.Inventory.d.array(name='kpoint_mesh', elementtype='int',
                                           shape=(3,), default= [0, 0, 0])
        kpoint_mesh.label = 'Monkhorst Pack Mesh'
        kpoint_mesh.help = '''triplet representing Monkhorst Pack mesh 
for integrating the Brillouin zone'''
        dosdispersionfile = Gulp.Inventory.d.str('dosdispersionfile', default = "gulp.phonons")
        dosdispersionfile.label = 'Filename for DOS and/or Dispersion'
        broaden_dos = Gulp.Inventory.d.bool('broaden_dos', default = False)
        broaden_dos.label = 'Broaden the DOS?'
        
        project_dos = Gulp.Inventory.d.str('project_dos', default = '')
        project_dos.label = 'Project the DOS onto Species'
        project_dos.help = '''species names separated by spaces (i.e. H Li)'''   
    GulpPhonons.Inventory = Inventory
except:
    pass
