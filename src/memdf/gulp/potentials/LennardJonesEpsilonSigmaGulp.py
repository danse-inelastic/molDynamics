from memd.gulp.forcefields.TwoAtomPotential import TwoAtomPotential
from os import linesep

class LennardJonesEpsilonSigmaGulp(TwoAtomPotential):
    '''representation of the lennard-jones potential for gulp'''
    
    class Inventory(TwoAtomPotential.Inventory):
        import pyre.inventory as inv
        AFit = inv.str("Fit A", default = 'None')
        AFit.meta['tip'] = "whether to change this parameter during a fitting run"
        AFit.validator = inv.choice(['None','True','False'])
        rhoFit = inv.str("Fit rho", default = 'None')
        rhoFit.meta['tip'] = "whether to change this parameter during a fitting run"
        rhoFit.validator = inv.choice(['None','True','False'])
        CFit = inv.str("Fit C", default = 'None')
        CFit.meta['tip'] = "whether to change this parameter during a fitting run"
        CFit.validator = inv.choice(['None','True','False'])
                
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
            + str(self.potential["epsilon"])+' '\
            + str(self.potential["sigma"])+' '\
            + '0.0 ' + str(self.potential["cutoff"])+' '\
            + self.getIfDefinedSpace(self.i.epsilonFit)\
            + self.getIfDefinedSpace(self.i.sigmaFit) + linesep

                