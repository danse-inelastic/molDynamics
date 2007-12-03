from molDynamics.gulp.forcefields.OneAtomPotential import OneAtomPotential
from os import linesep

class SpringGulp(OneAtomPotential):
    '''representation of spring potential for gulp'''
    class Inventory(OneAtomPotential.Inventory):
        import pyre.inventory as inv
        k2Fit = inv.str("Fit k2", default = 'None')
        k2Fit.meta['tip'] = "whether to change this parameter during a fitting run"
        k2Fit.validator = inv.choice(['None','True','False'])
                
    def __init__(self, atom1):
        OneAtomPotential.__init__(self, atom1)
        self.i=self.inventory
        
    def write(self):
        'writes the potential'
        return "spring "\
            + self.i.atom1+' '\
            + str(self.potential["k2"])+' '\
            + self.getIfDefinedSpace(self.i.k2Fit) + linesep
        
                