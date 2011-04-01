from memd.gulp.forcefields.TwoAtomPotential import TwoAtomPotential
from memd.gulp.forcefields.ForcefieldVisitor import Visitable

from os import linesep

class BuckinghamGulp(TwoAtomPotential,Visitable):
    '''representation of the buckingham potential for gulp'''
    
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
        
    def identify( self, visitor): 
        return visitor.writeBuckinghamGulp( self)
        

                