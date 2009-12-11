# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

class GulpResults:
    compressed_xyzTrajectory_filename = 'outputmovie.xyz.zip'
    xyzTrajectory_filename = 'outputmovie.xyz'
    output_filename = 'gulp.gout'
    dos_filename = 'dos.dens'

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  


# version
__id__ = "$Id$"

# End of file 
