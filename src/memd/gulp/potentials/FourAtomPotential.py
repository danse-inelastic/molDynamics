from interaction.FourAtomInteraction import FourAtomInteraction
from pyre.components.Component import Component

class FourAtomPotential(FourAtomInteraction):
    '''representation of a three atom potential for gulp'''
    class Inventory(Component.Inventory):
        import pyre.inventory as inv
        interIntra = inv.str( "Molecularity", default = 'None')
        interIntra.meta['tip'] = "whether the potential is molecular and if so, whether it is between or within molecules"
        interIntra.validator = inv.choice(['None','intermolecular','intramolecular'])
        bondXsO = inv.str( "Bonded Atom Interactions", default = 'None')
        bondXsO.meta['tip'] = "how the potential acts among bonded atoms"
        bondXsO.validator = inv.choice(['None',
                    'only between bonded atoms',
                    'not between bonded atoms',
                    'not between bonded atoms or atoms separated by two bonds',
                    'only between atoms separated by three bonds'])
        atom1 = inv.str('Atom 1',default='H')
        atom1.meta['tip'] = 'chemical species of atom 1'
        atom1.meta['importance'] = 100
        atom2 = inv.str('Atom 2',default='H')
        atom2.meta['tip'] = 'chemical species of atom 2'   
        atom2.meta['importance'] = 100
        atom3 = inv.str('Atom 3',default='H')
        atom3.meta['tip'] = 'chemical species of atom 3' 
        atom3.meta['importance'] = 100     
        atom4 = inv.str('Atom 4',default='H')
        atom4.meta['tip'] = 'chemical species of atom 4'  
        atom4.meta['importance'] = 100
        atom1Type = inv.str( "Atom 1 Type", default = 'core')
        atom1Type.meta['tip'] = "type of atom 1"
        atom1Type.validator = inv.choice(['core','shell'])
        atom1Type.meta['importance'] = 50
        atom2Type = inv.str( "Atom 2 Type", default = 'core')
        atom2Type.meta['tip'] = "type of atom 2"
        atom2Type.validator = inv.choice(['core','shell'])
        atom2Type.meta['importance'] = 50
        atom3Type = inv.str( "Atom 3 Type", default = 'core')
        atom3Type.meta['tip'] = "type of atom 3"
        atom3Type.validator = inv.choice(['core','shell'])
        atom3Type.meta['importance'] = 50
        atom4Type = inv.str( "Atom 4 Type", default = 'core')
        atom4Type.meta['tip'] = "type of atom 4"
        atom4Type.validator = inv.choice(['core','shell'])
        atom4Type.meta['importance'] = 50


    def __init__(self, atom1, atom2, atom3, atom4):
        FourAtomInteraction.__init__(self, atom1, atom2, atom3, atom4)
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
        
    def writeBonding(self):
        '''writes bonding options'''
        if self.i.bondXsO==None:
            return ''
        elif self.i.bondXs0=='only between bonded atoms':
            return 'bond '
        elif self.i.bondXs0=='not between bonded atoms':
            return 'x12 '
        elif self.i.bondXs0=='not between bonded atoms or atoms separated by two bonds':
            return 'x13 '
        elif self.i.bondXs0=='only between atoms separated by three bonds':
            return 'o14 '       
            
    def writeInterIntra(self):
        '''writes molecularity options'''
        if self.i.interIntra==None:
            return ''
        elif self.i.interIntra=='intermolecular':
            return 'inter '
        elif self.i.interIntra=='intramolecular':
            return 'intra '
        
    def getFlag(self, flagItem):
        if flagItem==None:
            return ''
        else:
            if flagItem:
                return '1 '
            else:
                return '0 '    
