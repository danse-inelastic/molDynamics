from memdf.gulp.Gulp import Gulp
class Fit(Gulp):
    '''This class fits forcefields to various experimental and ab initio quantities, which for now is mostly ab initio energies.'''
    constraints = 'None'
    energies = 'None'
    structures = 'None'
#    class Inventory(Component.Inventory):
#        import pyre.inventory as inv
#        constraints = inv.str('Constraints', default = 'None')
#        constraints.meta['tip'] = '''constraints on the cell'''
#        constraints.validator = inv.choice(['None', 'constant volume', 'constant pressure'])
#
#        energies = inv.facility('Ab initio Energies', default=InputFile('ab initio energies'))
#        energies.meta['tip'] = 'a pickled file containing a list of ab initio energies'
#
#        structures = inv.facility('Structures', default=InputFile('ab initio energies'))
#        structures.meta['tip'] = 'a pickled file containing a list of ab initio energies'
        
    def __init__(self, maverickObj=None,**kwds):
        Gulp.__init__(self, maverickObj, **kwds)
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        self.runTypeIdentifier='fit'
    
    def identifySettings(self, visitor):     
        return visitor.writeFitSettings(self)
    
    def writeKeywords(self, visitor): 
        keywords=[]
        keywords+=visitor.writeFitKeywords(self)
        keywords+=visitor.writeGulpKeywords(self)
        return keywords
    
    def writeOptions(self, visitor):
        options=''
        options+=visitor.writeGulpOptions(self)
        options+=visitor.writeFitOptions(self)
        return options