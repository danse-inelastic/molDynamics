# PyMOL interface
#
# Written by Konrad Hinsen
# last revision: 2002-8-21
#

try:

    from pymol import cmd
    from chempy import Atom, Bond, Molecule
    from chempy.models import Indexed

    def available():
        return 1

except ImportError:

    def available():
        return 0

import Units, Utility
import traceback


class Representation:

    def __init__(self, object, name = 'MMTK model', configuration = None):
        self.object = object
        self.universe = object.universe()
        self.name = name
        self.model = Indexed()
        self.index_map = {}
        self.atoms = []
        for o in object.bondedUnits():
            if Utility.isSequenceObject(o):
                groups = map(lambda g: (g, g.name), o)
            else:
                groups = [(o, None)]
            residue_number = 1
            for g, g_name in groups:
                for a in g.atomList():
                    atom = Atom()
                    atom.symbol = a.symbol
                    atom.name = a.name
                    if g_name is not None:
                        atom.resn = g_name
                        atom.resi = residue_number
                        residue_number = residue_number + 1
                    self.model.atom.append(atom)
                    self.index_map[a] = len(self.atoms)
                    self.atoms.append(a)
            for b in o.bonds:
                bond = Bond()
                bond.index = [self.index_map[b.a1], self.index_map[b.a2]]
                self.model.bond.append(bond)
        self._setCoordinates(configuration)

    def _setCoordinates(self, configuration):
        if configuration is None:
            for i in range(len(self.atoms)):
                self.model.atom[i].coord = \
                                  list(self.atoms[i].position()/Units.Ang)
        else:
            for i in range(len(self.atoms)):
                self.model.atom[i].coord = \
                                  list(configuration[self.atoms[i]]/Units.Ang)

    def show(self):
        cmd.load_model(self.model, self.name)

    def remove(self):
        cmd.delete(self.name)

    def update(self, configuration=None):
        try:
            cmd.set("suspend_updates","1")
            self._setCoordinates(configuration)
            cmd.load_model(self.model, self.name, 1)
        except:
            cmd.set("suspend_updates","0")
            traceback.print_exc()
        cmd.set("suspend_updates","0")
        cmd.refresh()

    def movie(self, configurations):
        n = 1
        for conf in configurations:
            self._setCoordinates(conf)
            cmd.load_model(self.model, self.name, n)
            n = n + 1
        cmd.mplay()
