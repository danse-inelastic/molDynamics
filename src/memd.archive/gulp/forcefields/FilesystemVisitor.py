class Visitable(object):
    
    def identify(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
    
class Visitor(object):
    
    def onFile(self, object):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)
        
    def onDirectory(self, object):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)



class File(Visitable):
    
    def __init__(self,name):
        self.name=name

    def identify( self, visitor): 
        return visitor.onFile( self)


class Directory(Visitable):
    
    def __init__(self,name):
        self.name=name

    def identify( self, visitor):
        return visitor.onDirectory( self)
    
#then read in some data structure and make a series of file and directory data objects
#then feed it to your Writer visitor
    
    
class Writer(Visitor):
    
    def onFile(self, object):
        print object.name
        
    def onDirectory(self, object):
        print object.name
        

def VisitorDemo():
    writer = Writer()



if __name__=='__main__':
    pass
    