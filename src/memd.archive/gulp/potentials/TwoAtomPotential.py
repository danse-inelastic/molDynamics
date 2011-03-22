from interaction.TwoAtomInteraction import TwoAtomInteraction
from pyre.components.Component import Component
from os import linesep

class TwoAtomPotential(TwoAtomInteraction):
    '''representation of a two atom potential for gulp'''
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
        scale14 = inv.str( "Scaling Options", default = 'None')
        scale14.meta['tip'] = "whether to scale certain potentials"
        scale14.validator = inv.choice(['None','scale interactions between atoms separated by three bonds'])
        atom1 = inv.str('Atom 1',default='H')
        atom1.meta['tip'] = 'chemical species of atom 1'
        atom1.meta['importance'] = 10
        atom2 = inv.str('Atom 2',default='H')
        atom2.meta['tip'] = 'chemical species of atom 2'  
        atom2.meta['importance'] = 10     
        atom1Type = inv.str( "Atom 1 Type", default = 'None')
        atom1Type.meta['tip'] = "type of atom 1"
        atom1Type.validator = inv.choice(['None', 'core','shell'])
        atom1Type.meta['importance'] = 5
        atom2Type = inv.str( "Atom 2 Type", default = 'None')
        atom2Type.meta['tip'] = "type of atom 2"
        atom2Type.validator = inv.choice(['None', 'core','shell'])
        atom2Type.meta['importance'] = 5
                
    def __init__(self, atom1, atom2):
        TwoAtomInteraction.__init__(self, atom1, atom2)
        self.i = self.inventory
        # initialize the atom types if the potential contains any
        
    def assignInteraction(self, name):
        self.potential = self.info[name]
        self.name = name
        if self.potential.has_key('atom1Type') and self.potential.has_key('atom2Type'):
            self.i.atom1Type = self.potential['atom1Type']
            self.i.atom2Type = self.potential['atom2Type']
    
    def getAssignedInteraction(self):
        return self.potential
            
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
            
    def writeBonding(self):
        '''writes bonding options'''
        
##         d = {
##             'only between bonded atoms': 'bond',
##             ....
##             }
##         return d[self.i.bondXs0]
        if self.i.bondXs0==None:
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
        
    def writeScaling(self):
        '''writes scaling options'''  
        if self.i.scale14==None:
            return ''
        elif self.i.scale14==None: 
            return
                
