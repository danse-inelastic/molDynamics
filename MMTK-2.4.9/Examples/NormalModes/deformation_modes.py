# This example shows how to calculate approximate low-frequency
# modes for big proteins. For a description of the techniques,
# see
#      K. Hinsen
#      Analysis of domain motions by approximate normal mode calculations
#      Proteins 33, 417 (1998)
#

from MMTK import *
from MMTK.Proteins import Protein
from MMTK.ForceFields import DeformationForceField
from MMTK.FourierBasis import FourierBasis, estimateCutoff
from MMTK.NormalModes import NormalModes, SubspaceNormalModes
from MMTK.Visualization import view

# Construct system
universe = InfiniteUniverse(DeformationForceField())
universe.protein = Protein('insulin.pdb', model='calpha')

# Find a reasonable basis set size and cutoff
nbasis = max(10, universe.numberOfAtoms()/5)
cutoff, nbasis = estimateCutoff(universe, nbasis)
print "Calculating %d low-frequency modes." % nbasis

if cutoff is None:
    # Do full normal mode calculation
    modes = NormalModes(universe)
else:
    # Do subspace mode calculation with Fourier basis
    subspace = FourierBasis(universe, cutoff)
    modes = SubspaceNormalModes(universe, subspace)

# Show animation of the first non-trivial mode
view(modes[6], 15.)
