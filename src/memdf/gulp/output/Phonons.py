
class Phonons:
    
    def __init__(self, cartesianConfiguration = [], kpoints = [], 
                 invcmFrequencies = [], modes = []):
        self.kpoints = kpoints
        self.invcmFrequencies = invcmFrequencies
        self.modes = modes
        
    def getRealModes(self):
        ''' here is the correct algorithm for making the eigenvectors
        real:
        abbreviated form: one needs to extend the supercell and multiply by phase factor
        and add together as complex conjugates until they are real
        (this is already implemented somewhere in isotropy--email stokes
        more later...
        
        for now we cheat and just take the real parts
        '''
        self.realModes = self.modes.real
        return self.realModes
    
    def writeVibrationsFile(self, filename):
        # output in modified xyz format
        f = file(filename)
        # get the initial configuration from the db
        
        # write to file
        #f.write(len()
        
    def getmevFrequencies(self):
        self.mevFrequencies = self.hbarTimesC*self.invcmFrequencies
        return self.mevFrequencies