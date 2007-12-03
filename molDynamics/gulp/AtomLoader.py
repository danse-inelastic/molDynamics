from pyre.components.Component import Component

class AtomLoader(Component):
    '''
Format:    atom no. x y z <<charge>> <<occupancy>> <<radius>> <<3 x optimisation flags>> <<%/T>> or at no. x y z <<charge>> <<occupancy>> <<radius>> <<3 x optimisation flags>> <<%/T>> or at.sym. <<species type>> x y z <<charge>> <<occupancy>> <<radius>> <<3 x flags>> <<%/T>>
Units:    Angstrom (default) or au for coordinates and electrons for charge, radius in Angstroms
Use:    Cartesian coordinates and charges for all species in the unit cell. Either the atomic number or the symbol may be supplied, followed by the species type. If the species type is omitted then it is assumed to be a core. Individual charges may be supplied for each ion or the charges for each type of species given using the species option. If the charges are given, then optionally site occupancies may also be specified. Optimisation flags are only needed if cellonly, conv, bulk, conp or shell are not specified. If the "region" sub-option is specified, then this tells the program the region number for the following atoms. In a surface calculation region 2 is held fixed. If the "rigid" sub-option is also specified after "region" then the region is created as a rigid body so that all atoms are constrained with respect to each other. By specifying a string after this containing x, y and/or z, the region may be allowed to move in particular directions. For example, in an interface calculation, a region could be specified that is allowed to only relax in the z direction by using:

cart region 3 rigid z

If a "T" is specified then the atom is marked for the translate option If a "%" is specified then the atom is part of a growth slice if it is in region 1 of a surface calculation.  
'''
    
    def __init__(self, name='atomLoader', facility='atoms'):
        Component.__init__(self, name, facility)
    
    def setText(self, text):
        self.text = text
        
    def getText(self):
        return self.text