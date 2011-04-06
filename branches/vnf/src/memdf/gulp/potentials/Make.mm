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

PROJECT = memdf
PACKAGE = gulp/potentials

#--------------------------------------------------------------------------
#

all: export


#--------------------------------------------------------------------------
#
# export

EXPORT_PYTHON_MODULES = \
	__init__.py \
	BuckinghamGulp.py \
	FourAtomPotential.py \
	LennardJonesABGulp.py \
	LennardJonesEpsilonSigmaGulp.py \
	MorseGulp.py \
	OneAtomPotential.py \
	SpringGulp.py \
	ThreeAtomPotential.py \
	ThreeBodyGulp.py \
	TorsionGulp.py \
	TwoAtomPotential.py \
	

    

export:: export-package-python-modules

# version
# $Id$

# End of file
