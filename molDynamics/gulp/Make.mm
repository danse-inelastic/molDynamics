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

PROJECT = molDynamics
PACKAGE = gulp

BUILD_DIRS = \
	forcefields \
	potentials \


	
OTHER_DIRS = \

RECURSE_DIRS = $(BUILD_DIRS) $(OTHER_DIRS)

#--------------------------------------------------------------------------
#

all: export
	BLD_ACTION="all" $(MM) recurse


#--------------------------------------------------------------------------
# export

EXPORT_PYTHON_MODULES = \
    __init__.py \
    AtomLoader.py \
    Coordinates.py \
    E.py \
    EigenDataParser.py \
    Fit.py \
    Gulp.py \
    KeywordWriter.py \
    LargeEigenDataParser.py \
    NetcdfPolarizationWrite.py \
    Optimize.py \
    OptionWriter.py \
    Phonon.py \
    PolarizationWrite.py \
    Potential.py \
    TrajectoryType.py \
    Visitable.py \
    Visitor.py \
    


export:: export-package-python-modules

# version
# $Id$

# End of file
