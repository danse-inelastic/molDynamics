from memdf.gulp.potentials.TwoAtomPotential import TwoAtomPotential
from pyre.components.Component import Component
from os import linesep

class LennardJonesABGulp(TwoAtomPotential):
    '''representation of the lennard-jones potential for gulp'''
    
    class Inventory(TwoAtomPotential.Inventory):
        import pyre.inventory as inv
        AFit = inv.str("Fit A", default = 'None')
        AFit.meta['tip'] = "whether to change this parameter during a fitting run"
        AFit.validator = inv.choice(['None','True','False'])
        BFit = inv.str("Fit B", default = 'None')
        BFit.meta['tip'] = "whether to change this parameter during a fitting run"
        BFit.validator = inv.choice(['None','True','False'])
                
    def __init__(self, atom1, atom2):
        TwoAtomPotential.__init__(self, atom1, atom2)
        self.i=self.inventory
        self.i.atom1 = atom1
        self.i.atom2 = atom2
        # add things to the repository
        
    def write(self):
        return "lennard epsilon "\
            + self.writeInterIntra()\
            + self.writeBonding()\
            + self.writeScaling()\
            + linesep\
            + self.i.atom1+' '\
            + self.i.atom1Type+' '\
            + self.i.atom2+' '\
            + self.i.atom2Type+' '\
            + str(self.potential["A"])+' '\
            + str(self.potential["B"])+' '\
            + '0.0 ' + str(self.potential["cutoff"])+' '\
            + self.getFlag(self.i.AFit)\
            + self.getFlag(self.i.BFit) + linesep

                