# -*- Makefile -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                        California Institute of Technology
#                        (C) 1998-2005 All Rights Reserved
#
# <LicenseText>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PROJECT = memd
PACKAGE = memd

PROJ_TIDY += *.log *.pyc
PROJ_CLEAN =


BUILD_DIRS = \


OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)


#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse

#--------------------------------------------------------------------------
#

#EXPORT_PYTHON_MODULES = \
#	__init__.py \
#	memd.py \

EXPORT_BINS = \
	memd.py \
	Memd.py \
	postProcessGulp.py \




export:: export-binaries release-binaries  #export-package-python-modules



# version
# $Id: Make.mm,v 1.5 2006/08/09 23:09:22 linjiao Exp $

# End of file
