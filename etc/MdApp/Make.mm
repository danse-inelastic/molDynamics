# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = MdApp

BUILD_DIRS = \


OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export

tidy::
	BLD_ACTION="tidy" $(MM) recurse

clean::
	BLD_ACTION="clean" $(MM) recurse

distclean::
	BLD_ACTION="distclean" $(MM) recurse
	
#--------------------------------------------------------------------------
# export

EXPORT_ETC = \
	amber.odb \
    fit.odb \
    gulp.odb \
    gulpLibrary.odb \
    lennardJones.odb \
    manualEntry.odb \
    md.odb \
    mmtk.odb \
    optimize.odb \
    phonon.odb \
    unitCellBuilder.odb \
    xyzFile.odb \



export:: export-etc


# version
# $Id: Make.mm,v 1.1 2006/08/03 23:42:43 linjiao Exp $

# End of file
