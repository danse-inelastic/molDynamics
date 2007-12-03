from MMTK import *
from HarmonicOscillatorFF import HarmonicOscilatorForceField

universe = InfiniteUniverse()
universe.atom1 = Atom('C', position=Vector(0., 0., 1.05))
universe.atom2 = Atom('C', position=Vector(0., 1.05, 0.))

ff1 = HarmonicOscilatorForceField(universe.atom1, Vector(0., 0., 1.), 100.)
ff2 = HarmonicOscilatorForceField(universe.atom2, Vector(0., 1., 0.), 100.)
universe.setForceField(ff1+ff2)

e, g = universe.energyAndGradients()
print universe.energyTerms()
print e
