from molDynamics.gulp.potentials.ThreeAtomPotential import ThreeAtomPotential
from os import linesep

class ThreeBodyGulp(ThreeAtomPotential):
    '''representation of a three atom potential for gulp'''
    
    class Inventory(ThreeAtomPotential.Inventory):
        import pyre.inventory as inv
        kFit = inv.str("Fit k", default = 'None')
        kFit.meta['tip'] = "whether to change this parameter during a fitting run"
        kFit.validator = inv.choice(['None','True','False'])
        theta0Fit = inv.str("Fit theta0", default = 'None')
        theta0Fit.meta['tip'] = "whether to change this parameter during a fitting run"
        theta0Fit.validator = inv.choice(['None','True','False'])
                
    def __init__(self, atom1, atom2, atom3):
        ThreeAtomPotential.__init__(self, atom1, atom2, atom3)
        self.i=self.inventory
        self.i.atom1 = atom1
        self.i.atom2 = atom2
        self.i.atom3 = atom3

            
    def getIfDefined(self, inventoryItem):
        if inventoryItem==None:
            return ''
        else:
            return inventoryItem
        
    def getIfDefinedSpace(self, inventoryItem):
        if inventoryItem==None:
            return ''
        else:
            return inventoryItem+' '
        
    def write(self):
        '''write the potential'''
        #note gulp requires the middle atom be printed first
        return "three "\
            + self.writeInterIntra()\
            + self.writeBonding()\
            + linesep\
            + self.i.atom2+' '\
            + self.i.atom2Type+' '\
            + self.i.atom1+' '\
            + self.i.atom1Type+' '\
            + self.i.atom3+' '\
            + self.i.atom3Type+' '\
            + str(self.potential["k"])+' '\
            + str(self.potential["theta0"])+' '\
            + str(self.potential["cutoff"][0])+' '\
            + str(self.potential["cutoff"][1])+' '\
            + str(self.potential["cutoff"][2])+' '\
            + self.getFlag(self.i.kFit)\
            + self.getFlag(self.i.theta0Fit)\
            + linesep
