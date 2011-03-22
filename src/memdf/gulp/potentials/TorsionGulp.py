from molDynamics.gulp.potentials.FourAtomPotential import FourAtomPotential
from os import linesep

class TorsionGulp(FourAtomPotential):
    '''representation of a three atom potential for gulp'''
    
    class Inventory(FourAtomPotential.Inventory):
        import pyre.inventory as inv
        kFit = inv.str("Fit k", default = 'None')
        kFit.meta['tip'] = "whether to change this parameter during a fitting run"
        kFit.validator = inv.choice(['None', 'True', 'False'])

                
    def __init__(self, atom1, atom2, atom3, atom4):
        FourAtomPotential.__init__(self, atom1, atom2, atom3, atom4)
        self.i=self.inventory
        self.i.atom1 = atom1
        self.i.atom2 = atom2
        self.i.atom3 = atom3
        self.i.atom4 = atom4
        
    def write(self):
        '''writes the potential out'''
        return "torsion "\
            + self.writeInterIntra()\
            + self.writeBonding()\
            + linesep\
            + self.i.atom1+' '\
            + self.i.atom1Type+' '\
            + self.i.atom2+' '\
            + self.i.atom2Type+' '\
            + self.i.atom3+' '\
            + self.i.atom3Type+' '\
            + self.i.atom4+' '\
            + self.i.atom4Type+' '\
            + str(self.potential["k"])+' '\
            + str(self.potential["isign"])+str(self.potential["n"])+' '\
            + str(self.potential["cutoff"][0])+' '\
            + str(self.potential["cutoff"][1])+' '\
            + str(self.potential["cutoff"][2])+' '\
            + str(self.potential["cutoff"][3])+' '\
            + self.getFlag(self.i.kFit)\
            + linesep
