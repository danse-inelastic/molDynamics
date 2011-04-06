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

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	AtomLoader.py \
	Coordinates.py \
	E.py \
	Fit.py \
	GulpPotential.py \
	Gulp.py \
	GulpResults.py \
	GulpSettings.py \
	__init__.py \
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
