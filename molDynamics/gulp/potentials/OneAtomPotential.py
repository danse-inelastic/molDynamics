from interaction.OneAtomInteraction import OneAtomInteraction
from pyre.components.Component import Component

class OneAtomPotential(OneAtomInteraction):
    '''representation of a one atom potential for gulp'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        atom1 = inv.str('Atom 1',default='H')
        atom1.meta['tip'] = 'chemical species of atom 1'
        atom1.meta['importance'] = 10
#        atom1Type = inv.str( "Atom 1 Type", default = 'core')
#        atom1Type.meta['tip'] = "type of atom 1"
#        atom1Type.validator = inv.choice(['core','shell'])
#        atom1Type.meta['importance'] = 5
                
    def __init__(self, atom1):
        OneAtomInteraction.__init__(self, atom1)
#        self.atom1 = atom1
#        self.atom2 = atom2
        self.i=self.inventory
            
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
        
    def getFlag(self, flagItem):
        if flagItem==None:
            return ''
        else:
            if flagItem:
                return '1 '
            else:
                return '0 '
        
    def write(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
        
                