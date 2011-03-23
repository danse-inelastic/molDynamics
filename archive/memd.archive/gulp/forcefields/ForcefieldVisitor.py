from os import linesep

class Visitable(object):
    
    def identify(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
    
class Visitor(object):
    
    pass

#for forcefields there will be the forcefield itself and the individual potentials

#class File(Visitable):
#    
#    def __init__(self,name):
#        self.name=name
#
#class Directory(Visitable):
#    
#    def __init__(self,name):
#        self.name=name
#
#    def identify( self, visitor):
#        return visitor.onDirectory( self)
    
#then read in some data structure and make a series of file and directory data objects
#then feed it to your ForcefieldWriter visitor and your ForcefieldArchiver visitor
    
class ForcefieldWriter(Visitor):
    
    def onForcefield(self, forcefield):
        self.writeBuckinghamGulp(potObject)
        
    def writeBuckinghamGulp(self,potObject):
        return "buckingham "\
            + potObject.writeInterIntra()\
            + potObject.writeBonding()\
            + potObject.writeScaling()\
            + linesep\
            + potObject.i.atom1+' '\
            + potObject.i.atom1Type+' '\
            + potObject.i.atom2+' '\
            + potObject.i.atom2Type+' '\
            + str(potObject.potential["A"])+' '\
            + str(potObject.potential["rho"])+' '\
            + str(potObject.potential["C"])+' '\
            + '0.0 ' + str(potObject.potential["cutoff"])+' '\
            + potObject.getFlag(potObject.i.AFit)\
            + potObject.getFlag(potObject.i.rhoFit)\
            + potObject.getFlag(potObject.i.CFit)\
            + linesep
        

def VisitorDemo():
    writer = Writer()



if __name__=='__main__':
    pass
    