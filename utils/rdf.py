from MMTK import *
from MMTK.Trajectory import Trajectory
from Scientific.IO import ArrayIO
from Scientific.Statistics.Histogram import Histogram
from Gnuplot import plot
import Numeric


class PairDistributionFunction:

    def __init__(self, object, upper_limit, bin_width):
        from MMTK_forcefield import NonbondedList
        self.object = object
        self.universe = object.universe()
        self.upper_limit = upper_limit
        empty = Numeric.zeros((0, 2), Numeric.Int)
        atoms = Numeric.array(map(lambda a: a.index, object.atomList()))
        self.nblist = NonbondedList(empty, empty, atoms, universe._spec,
                                    upper_limit)
        self.nbins = int(upper_limit/bin_width)
        self.bin_width = bin_width

    def __call__(self):
        self.nblist.update(self.universe.configuration().array)
        d = self.nblist.pairDistances()
        h = Histogram(d, self.nbins, (0., self.upper_limit)).array
        natoms = self.object.numberOfAtoms()
        density = natoms/self.universe.cellVolume()
        h[:,1] = h[:,1]/(2.*Numeric.pi*h[:,0]**2*self.bin_width*density*natoms)
        return h

t = Trajectory(None, "water.nc")
universe = t.universe
oxygens = universe.map(lambda m: m.O)

bin_width = 0.005
r_max = 1.2

gr = PairDistributionFunction(oxygens, r_max, bin_width)

g = 0.
nconf = 0
for step in range(0, len(t), 5):
    universe.setFromTrajectory(t, step)
    g = g + gr()
    nconf = nconf + 1
g = g/nconf
ArrayIO.writeArray(g, "gr.plot")
plot(g)