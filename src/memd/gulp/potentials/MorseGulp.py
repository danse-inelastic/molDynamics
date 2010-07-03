from memd.gulp.potentials.TwoAtomPotential import TwoAtomPotential
from pyre.components.Component import Component
from os import linesep

class MorseGulp(TwoAtomPotential):
    '''representation of the lennard-jones potential for gulp'''
    
    class Inventory(TwoAtomPotential.Inventory):
        import pyre.inventory as inv
        DFit = inv.str("Fit D", default = 'None')
        DFit.meta['tip'] = "whether to change this parameter during a fitting run"
        DFit.validator = inv.choice(['None','True','False'])
        aFit = inv.str("Fit a", default = 'None')
        aFit.meta['tip'] = "whether to change this parameter during a fitting run"
        aFit.validator = inv.choice(['None','True','False'])
        r0Fit = inv.str("Fit r0", default = 'None')
        r0Fit.meta['tip'] = "whether to change this parameter during a fitting run"
        r0Fit.validator = inv.choice(['None','True','False'])
                
    def __init__(self, atom1, atom2):
        TwoAtomPotential.__init__(self, atom1, atom2)
        self.i=self.inventory
        self.i.atom1 = atom1
        self.i.atom2 = atom2
        # add things to the repository
        
    def write(self):            
        return "morse "\
            + self.writeInterIntra()\
            + self.writeBonding()\
            + self.writeScaling()\
            + linesep\
            + self.i.atom1+' '\
            + self.i.atom1Type+' '\
            + self.i.atom2+' '\
            + self.i.atom2Type+' '\
            + str(self.potential["D"])+' '\
            + str(self.potential["a"])+' '\
            + str(self.potential["r0"])+' '\
            + '0.0 ' + str(self.potential["cutoff"])+' '\
            + self.getFlag(self.i.DFit)\
            + self.getFlag(self.i.aFit)\
            + self.getFlag(self.i.r0Fit) + linesep

                