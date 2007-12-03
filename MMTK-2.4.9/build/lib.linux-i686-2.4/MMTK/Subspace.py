# This module implements subspaces for motion analysis etc.
#
# Written by Konrad Hinsen
# last revision: 2007-3-22
#

"""This module implements subspaces for infinitesimal (or finite
small-amplitude) atomic motions. They can be used in normal mode
calculations (see example Example:NormalModes:constrained_modes.py) or
for analyzing complex motions [Article:Hinsen1999a].
"""

import Utility, ParticleProperties
from Scientific.Geometry import Vector
import Numeric

#
# Import LAPACK routines
#
dgesdd = None
try:
    # Numeric
    from lapack_lite import dgesdd, LapackError
except ImportError: pass
if dgesdd:
    n = 1
    array = Numeric.zeros((n, n), Numeric.Float)
    sv = Numeric.zeros((n,), Numeric.Float)
    u = Numeric.zeros((n, n), Numeric.Float)
    vt = Numeric.zeros((n, n), Numeric.Float)
    work = Numeric.zeros((1,), Numeric.Float)
    int_types = [Numeric.Int, Numeric.Int8, Numeric.Int16, Numeric.Int32]
    try:
        int_types.append(Numeric.Int64)
        int_types.append(Numeric.Int128)
    except AttributeError:
        pass
    for int_type in int_types:
        iwork = Numeric.zeros((1,), int_type)
        try:
            dgesdd('S', n, n, array, n, sv, u, n, vt, n, work, -1, iwork, 0)
            break
        except LapackError:
            pass
    del n, array, sv, u, vt, work, iwork, int_types

#
# A set of particle vectors that define a subspace
#
class ParticleVectorSet:

    def __init__(self, universe, data):
        self.universe = universe
        if type(data) == Numeric.arraytype:
            self.n = data.shape[0]
            self.array = data
        else:
            self.n = data
            self.array = Numeric.zeros((self.n, universe.numberOfAtoms(), 3),
                                       Numeric.Float)

    def __len__(self):
        return self.n

    def __getitem__(self, i):
        if i >= self.n:
            raise IndexError
        return ParticleProperties.ParticleVector(self.universe, self.array[i])


class Subspace:

    """Subspace of infinitesimal atomic motions

    Constructor: Subspace(|universe|, |vectors|)

    Arguments:

    |universe| -- the universe for which the subspace is created

    |vectors| -- a list of Class:MMTK.ParticleVector objects
                 that define the subspace. They need not be orthogonal
                 or linearly independent.
    """

    def __init__(self, universe, vectors):
        self.universe = universe
        self.vectors = vectors
        self._basis = None

    def __add__(self, other):
        return Subspace(self.vectors+other.vectors)

    def __len__(self):
        return len(self.vectors)

    def __getitem__(self, item):
        return self.vectors[item]

    def getBasis(self):
        """Returns a basis for the subspace, which is obtained
        by orthonormalization of the input vectors using Singular
        Value Decomposition. The basis consists of a sequence
        of Class:MMTK.ParticleVector objects that are orthonormal
        in configuration space."""
        if self._basis is None:
            basis = Numeric.array(self.vectors, Numeric.Float)
            shape = basis.shape
            nvectors = shape[0]
            natoms = shape[1]
            basis.shape = (nvectors, 3*natoms)
            sv = Numeric.zeros((min(nvectors, 3*natoms),), Numeric.Float)
            min_n_m = min(3*natoms, nvectors)
            u = Numeric.zeros((min_n_m, 3*natoms), Numeric.Float)
            vt = Numeric.zeros((nvectors, min_n_m), Numeric.Float)
            work = Numeric.zeros((1,), Numeric.Float)
            iwork = Numeric.zeros((8*min_n_m,), int_type)
            result = dgesdd('S', 3*natoms, nvectors, basis, 3*natoms,
                            sv, u, 3*natoms, vt, min_n_m,
                            work, -1, iwork, 0)
            work = Numeric.zeros((int(work[0]),), Numeric.Float)
            result = dgesdd('S', 3*natoms, nvectors, basis, 3*natoms,
                            sv, u, 3*natoms, vt, min_n_m,
                            work, work.shape[0], iwork, 0)
            if result['info'] != 0:
                raise ValueError('Lapack SVD: ' + `result['info']`)
            svmax = Numeric.maximum.reduce(sv)
            nvectors = Numeric.add.reduce(Numeric.greater(sv, 1.e-10*svmax))
            u = u[:nvectors]
            u.shape = (nvectors, natoms, 3)
            self._basis = ParticleVectorSet(self.universe, u)
        return self._basis

    def projectionOf(self, vector):
        """Returns the projection of |vector| (a Class:MMTK.ParticleVector
        object) onto the subspace."""
        vector = vector.array
        basis = self.getBasis().array
        p = Numeric.zeros(vector.shape, Numeric.Float)
        for bv in basis:
            Numeric.add(Numeric.add.reduce(Numeric.ravel(bv*vector))*bv, p, p)
        return ParticleProperties.ParticleVector(self.universe, p)

    def projectionComplementOf(self, vector):
        """Returns the projection of |vector| (a Class:MMTK.ParticleVector
        object) onto the orthogonal complement of the subspace."""
        return vector - self.projectionOf(vector)


class RigidMotionSubspace(Subspace):

    """Subspace of rigid-body motions

    A Glossary:Subclass of Class:MMTK.Subspace.Subspace.

    A rigid-body motion subspace is the subspace which contains
    the rigid-body motions of any number of chemical objects.

    Constructor: RigidMotionSubspace(|universe|, |objects|)

    Arguments:

    |universe| -- the universe for which the subspace is created

    |objects| -- a sequence of objects whose rigid-body motion is
                 included in the subspace
    """

    def __init__(self, universe, objects):
        if not Utility.isSequenceObject(objects):
            objects = [objects]
        vectors = []
        for o in objects:
            atoms = o.atomList()
            for d in [Vector(1.,0.,0.), Vector(0.,1.,0.), Vector(0.,0.,1.)]:
                v = ParticleProperties.ParticleVector(universe)
                for a in atoms:
                    v[a] = d
                vectors.append(v/Numeric.sqrt(len(atoms)))
            if len(atoms) > 1:
                center = o.centerOfMass()
                iv = len(vectors)-3
                for d in [Vector(1.,0.,0.),Vector(0.,1.,0.),Vector(0.,0.,1.)]:
                    v = ParticleProperties.ParticleVector(universe)
                    for a in atoms:
                        v[a] = d.cross(a.position()-center)
                    for vt in vectors[iv:]:
                        v = v - v.dotProduct(vt)*vt
                    vectors.append(v/Numeric.sqrt(v.dotProduct(v)))
        Subspace.__init__(self, universe, vectors)
        # The vector set is already orthonormal by construction
        # (assuming that the rigid bodies have no atoms in common),
        # so we can eliminate the lengthy SVD procedure
        count = ParticleProperties.ParticleScalar(universe)
        for o in objects:
            count = count + o.booleanMask()
        if Numeric.maximum.reduce(count.array) == 1:
            self._basis = ParticleVectorSet(universe, len(vectors))
            for i in range(len(vectors)):
                self._basis.array[i] = vectors[i].array


class PairDistanceSubspace(Subspace):

    """Subspace of pair-distance motions

    A Glossary:Subclass of Class:MMTK.Subspace.Subspace.

    A pair-distance motion subspace is the subspace which contains
    the relative motions of any number of atom pairs along
    their distance vector, e.g. bond elongation between two
    bonded atoms.

    Constructor: PairDistanceSubspace(|universe|, |atom_pairs|)

    Arguments:

    |universe| -- the universe for which the subspace is created

    |atom_pairs| -- a sequence of atom pairs whose distance-vector
                    motion is included in the subspace
    """

    def __init__(self, universe, atom_pairs):
        vectors = []
        for atom1, atom2 in atom_pairs:
            v = ParticleProperties.ParticleVector(universe)
            distance = atom1.position()-atom2.position()
            v[atom1] = distance
            v[atom2] = -distance
            vectors.append(v)
        Subspace.__init__(self, universe, vectors)
