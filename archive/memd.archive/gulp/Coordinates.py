#!/usr/bin/env python
# =================================================================
#
# {LicenseText}
#
# =================================================================
#
from os import linesep
  
class Coordinates:
    """class representing the coordinates """
  
    def __init__(self, inventory):
        self.sample = inventory.sample
        self.i = inventory
        self.atoms=eval(self.i.sample.i.atomicStructure.i.atoms)
        self.partialCharges=eval(self.i.sample.i.partialCharges)
        #do several hierarchies of writing coordinates, just like GULP does it
#        sampleItems = self.sample.i.atoms=__dict__.keys()
#        if 'atoms' not in sampleItems: 
#            print 'please put atoms in the sample'
#            sys.exit()
        #possibleEntries=['atoms','partialCharges']
        #hierarchy 1: just coordinates
#        if ('partialCharges' not in sampleItems) and (not self.i.optimizeCoordinates):
#            self.write = self.writeSimple  
#        #hierarchy 2: atoms and partial charges
#        if ('partialCharges' in sampleItems) and (not self.i.optimizeCoordinates):
#            self.write = self.writePartialCharges
#        #hierarchy 3: atoms and atomic fitting flags
#        if ('partialCharges' not in sampleItems) and self.i.optimizeCoordinates:
#            # assume partialCharges are all zero
#            numAtoms = len(self.sample.atoms)
#            self.sample.partialCharges=[0.0 for i in numAtoms]
#            self.write = self.writeFitting
#        #hierarchy 4: atoms and partial charges and atomic fitting flags
#        if ('partialCharges' in sampleItems) and self.i.optimizeCoordinates:
#            self.write = self.writeFitting
        # initialize
        #self.coordinateLines = 'cartesian '+str(len(self.sample.atoms))+linesep
        #rewrite of above:
        # the whole reason this must be written this way is because fitting flags require that
        # the partial charges are written first before gulp recognizes them--it's crazy
        if self.partialCharges==None:
            #hierarchy 3: atoms and atomic fitting flags
            if self.i.optimizeCoordinates:
                 # assume partialCharges are all zero and write them
                numAtoms = len(self.atoms)
                self.partialCharges=[0.0 for i in numAtoms]
                self.write = self.writeFitting
            #hierarchy 1: just coordinates
            else:
                self.write = self.writeSimple 

        if self.partialCharges!=None:
            #hierarchy 4: atoms and partial charges and atomic fitting flags
            if self.i.optimizeCoordinates:
                self.write = self.writeFitting
            #hierarchy 2: atoms and partial charges
            else:
                self.write = self.writePartialCharges

    def writeSimple(self):
        '''writes out cartesian coordinates for all atoms'''
        self.coordinateLines = self.i.coordinateFormat+' '+str(len(self.atoms))+linesep
        for atom in self.atoms:
                self.coordinateLines+=atom[0]+' '+str(atom[1])+' '+str(atom[2])+' '+str(atom[3])+linesep
        return self.coordinateLines
    
    def writePartialCharges(self):
        '''writes out cartesian coordinates for all atoms'''
        self.coordinateLines = self.i.coordinateFormat+' '+str(len(self.atoms))+linesep
        for atom in self.atoms:
            self.coordinateLines+=atom[0]+' '+str(atom[1])+' '+str(atom[2])+' '\
                    +str(atom[3])+' '+str(self.partialCharges[atom[0]])+linesep
        return self.coordinateLines
    
    
    def writeFitting(self):
        '''writes out cartesian coordinates for all atoms'''
        self.coordinateLines = self.i.coordinateFormat+' '+str(len(self.atoms))+linesep
        firstAtom=self.atoms[0]
        for atom in self.atoms:
            self.coordinateLines+=atom[0]+' '+str(atom[1])+' '+str(atom[2])+' '\
                +str(atom[3])+' '+str(self.partialCharges[atom[0]])+' '
            if atom==firstAtom:
                self.coordinateLines+='0 0 0'+linesep
            else:
                self.coordinateLines+='1 1 1'+linesep
        return self.coordinateLines
    
# version
__id__ = "$Id$"
 
# End of file