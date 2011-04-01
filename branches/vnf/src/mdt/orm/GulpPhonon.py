#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                         J Brandon Keith, Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011 All Rights Reserved  
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from ..GulpPhonon import GulpPhonon
from Gulp import Gulp

        
class Inventory(Gulp.Inventory):
    kpoint_mesh = Gulp.Inventory.d.array(name='kpoint_mesh', elementtype='int',
                                       shape=(3,), default= [0, 0, 0])
    kpoint_mesh.label = 'Monkhorst Pack Mesh'
    kpoint_mesh.help = '''triplet representing Monkhorst Pack mesh for integrating the Brillouin zone'''
    
    # XXX: see Gulp.py
    # dosdispersionfile = Gulp.Inventory.d.str(name='dosdispersionfile', default = "gulp.phonons") 
    # dosdispersionfile.label = 'Filename for DOS and/or Dispersion'

    broaden_dos = Gulp.Inventory.d.bool(name='broaden_dos', default = False)
    broaden_dos.label = 'Broaden the DOS?'

    project_dos = Gulp.Inventory.d.str(name='project_dos', default = '')
    project_dos.label = 'Project the DOS onto Species'
    project_dos.help = '''species names separated by spaces (i.e. H Li)'''   
GulpPhonon.Inventory = Inventory


def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['properties', 'forcefield']
    drawer.mold.sequence = [
        'kpoint_mesh',
        'broaden_dos',
        'project_dos',
        'temperature', 'pressure', 
        'identify_molecules',
        'assign_bonds_from_initial_geometry',
        'calc_dispersion_in_recip_space',
        ]
    return
GulpPhonon.customizeLubanObjectDrawer = customizeLubanObjectDrawer
