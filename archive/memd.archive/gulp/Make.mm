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

PROJECT = memd
PACKAGE = gulp

BUILD_DIRS = \
	forcefields \
	output \
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
    GulpPotential.py \
    GulpResults.py \
    GulpSettings.py \
    KeywordWriter.py \
    Md.py \
    MdX.py \
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
