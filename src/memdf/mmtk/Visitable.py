

class Visitable(object):
    
    def identify(self):
        raise NotImplementedError("class %r must override 'execute'" % self.__class__.__name__)