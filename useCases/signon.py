#!/usr/bin/env python
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
# 
#  <LicenseText>
# 
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 

if __name__ == "__main__":

    import molDynamics
    from molDynamics import molDynamics as molDynamicsmodule

    print "copyright information:"
    print "   ", molDynamics.copyright()
    print "   ", molDynamicsmodule.copyright()

    print
    print "module information:"
    print "    file:", molDynamicsmodule.__file__
    print "    doc:", molDynamicsmodule.__doc__
    print "    contents:", dir(molDynamicsmodule)

    print
    print molDynamicsmodule.hello()

# version
__id__ = "$Id$"

#  End of file 
