from pyparsing import *
import pickle
import numpy as np
from os import sep
import re, sys
import urllib
#import scipy.io
from memd.gulp.E import write as writeEs
#from memd.gulp.NetcdfPolarizationWrite import NetcdfPolarizationWrite

# numbers: 1, 30.0, 1e-5, -99
number = Combine( Optional('-') + ( '0' | Word('123456789',nums) ) + \
                  Optional( '.' + Word(nums) ) + \
                  Optional( Word('eE',exact=1) + Word(nums+'+-',nums) ) )

digits = "0123456789"
integer = Word(digits)

def convertNumbers(s,l,toks):
    n = toks[0]
    try: return int(n)
    except ValueError, ve: return float(n)
    raise

number.setParseAction( convertNumbers )
integer.setParseAction( convertNumbers )

threeNums = Group(number + number + number)
vecLine = Group(integer + Word(alphas) + threeNums + threeNums)

frequencyLine = Suppress(Literal("Frequency")) + number + number + number

eigAndVec = frequencyLine + \
  Suppress(Literal("Real    Imaginary   Real    Imaginary   Real    Imaginary")) + \
  OneOrMore(vecLine)

eigsAndVecs = OneOrMore(eigAndVec)

class OutputParser:
    
    hbarTimesC=6.58211899e-16*1e3*29.978*1e9#hbar eV*s * 1 meV/eV * c cm/s = hbarTimesC meV*cm
    parsingEigenvalues=False
    
    def __init__(self, gulpOutputFile='', runtype = 'molecular dynamics', 
                 inventory='',EsFilename="Es.dat", 
                 polarizationsFilename="Polarizations.nc",
                 memoryModel='storeInternally'):
        # if output files are expected to be large, set memoryModel we must parse only the parts we want and 
        # immediately extract them and put them in the desired return format
        
        # perhaps the best way to do this for now is to parse the file each time for each quantity 
        # you want since gulp output files tend to be free of unnecessary clutter

        # so eventually take the inventory and decide which values have been set and look for them (or have an object 
        # which has this information encoded)
        self.removeNegativeFrequencies = True # eventually put in a way to remove negative frequencies
        self.convertToEnergies = True
        self.gulpOutputFile = gulpOutputFile
        self.EsFilename = EsFilename
        #temp=file(inventory.sample.i.atomicStructure.i.xyzFile.i.inputFile)
        self.numAtoms = self.parseNumAtoms()
#        self.numAtoms=1116#int(temp.readline())
        self.runtype = runtype

        if 'phonons' in runtype:
            self.numModes = 3*self.numAtoms
            self.numKpoints, self.kpoints = self.parseKpoints()
        elif 'molecular dynamics' in runtype:
            pass
#        self.pWrite=PolarizationWrite(filename=polarizationsFilename, 
#                                numAtoms=self.numAtoms, numks=self.numKpoints)
#        self.polWrite=NetcdfPolarizationWrite(filename=polarizationsFilename, 
#                                numks=self.numKpoints, numAtoms=self.numAtoms)

#    def _getGulpOutput(self):
#        if !self.gulpOutput:
#            
#            return urllib.urlopen(self.gulpOutputFile)
#        else
#            
#    gulpOutput = property(_getGulpOutput())
        
    def _parseInitialConfiguration(self):
        '''gets the initial configuration from gulp's output file
        
        The reason one would want to get the configuration from the output
        file instead of from the database is because in gulp the original
        configuration is frequently altered, such as when creating a supercell.'''
        
        gulpOutput = urllib.urlopen(self.gulpOutputFile)
        self._initialConfiguration=[]
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                break
            if 'Frequency' in line:
                #print frequencyLine.parseString(line)
                #if frequencyLine.parseString(line):
                space_re='[ \t]+'
                float_re='[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
                if re.search('Frequency' + space_re + float_re + space_re + float_re + space_re + float_re, line):
                    self.eigs += map(lambda x: float(x),(line.split())[1:])
            if modeIndex==self.numModes:
                kpointIndex+=1
                modeIndex=0  
               
    @property 
    def initialConfiguration(self):
        '''retrieve the initial configuration'''
        if not hasattr(self, '_initialConfiguration'):
            self.parseInitialConfiguration()
        return self._initialConfiguration
        
        
    def _initializePhonons(self):
        from vsat.Phonons import Phonons
        phonons = Phonons()
        phonons.kptList = self.getKpoints()
        return phonons
    
    def _reshapeEigenData(self, eigVals=None, eigVecs=None):
        '''since kpoints will be in the same order as the eigs/vecs, we 
        simply get corresponding eigs/vecs

        attention: this only works for gulp mesh, which 
        appears to be in lexicographic order.
        Thus we can do a naive resort with the z axis on the innermost
        index and changing the fastest.
        '''
        eigVals = np.array(eigVals)
        eigVecs = np.array(eigVecs)
        #reshape in k mesh
        mx,my,mz = self.kpointMesh
        eigVals.reshape((mx, my, mz, self.numModes))
        #reshape in groups of k, number of modes, and polarization vector per atom
        eigVecs.reshape((self.numKpoints, self.numModes, self.numAtoms, 3))
        return eigVals, eigVecs

    def getEigvals(self):
        '''finds and returns all eigenvalues in a list, along with kpts
        
        the eigenvalues are reshaped according to (numKpoints, numModes)
        where numModes = 3*numAtoms
        '''
        gulpOutput = urllib.urlopen(self.gulpOutputFile)               
        phonons = self._initializePhonons()
        eigs = []
#        vecs = []
        kpointIndex = 0
        modeIndex = 0
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                break
            if 'Frequencies' in line:
                kpointEigs=[]
                gulpOutput.readline()
                # now keep parsing until get blankline
                eigvals = gulpOutput.readline().split()
                while len(eigvals)>0:
                    kpointEigs += map(float, eigvals)
                    eigvals = gulpOutput.readline().split()
                eigs.append(kpointEigs)
            if modeIndex == self.numModes:
                kpointIndex += 1
                modeIndex = 0
        gulpOutput.close()
        phonons.eigVals = np.array(eigs)
        phonons.
        return phonons

    def getEigsAndVecs(self):
        '''finds and returns all eigenvectors and eigenvalues in a list with 
        kpts--eventually will use a "smart algorithm" that looks at the size of the
        output file and gauges whether or not to write them to file or return them
        
        the eigenvalues are reshaped according numKpoints, numModes
        the eigenvecs are reshaped according to numKpoints, numModes, numModes
        
        where numModes = 3*numAtoms
        '''
        gulpOutput = urllib.urlopen(self.gulpOutputFile)  
        phonons = self._initializePhonons()             
        eigs = []
        vecs = []
        kpointIndex = 0
        modeIndex = 0
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                break
            if 'Frequency' in line:
                #print frequencyLine.parseString(line)
                #if frequencyLine.parseString(line):
                space_re = '[ \t]+'
                float_re = '[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
                if re.search('Frequency' + space_re + float_re + space_re + float_re + space_re + float_re, line):
                    eigs += map(lambda x: float(x),(line.strip().split())[1:])
            elif 'Real    Imaginary   Real    Imaginary   Real    Imaginary' in line:
                gulpOutput.readline()
                vecs += self._getComplexVecs(kpointIndex,modeIndex,gulpOutput)
                modeIndex += 3
                #print 'eigenDataParser wrote kpoint, mode',kpointIndex,modeIndex
#                eigs.append(eig)
            if modeIndex == self.numModes:
                kpointIndex += 1
                modeIndex = 0
        gulpOutput.close()
        #reshape according to the number of kpoints
        phonons.eigVals,phonons.eigVecs =self.reshapeEigenData(eigs,vecs)
        return phonons 
        
#    def getPhononModes(self, scaleDisplacementsByEigenvalues = True):
#        eigsNVecs = self.getEigsAndVecs()

    def outputVibrationsFile(self, filename):
        phonons = self.getEigsAndVecs()
        phonons.writeVibrationsFile(filename)

    def writeVecs(self,kpointIndex, modeIndex, gulpOutputFileDescriptor):
        mode1,mode2,mode3 = self.getVecs(kpointIndex, modeIndex, gulpOutputFileDescriptor)
        self.polWrite.writeVec(mode1)
        self.polWrite.writeVec(mode2)
        self.polWrite.writeVec(mode3)

    def getVecs(self, kpointIndex, modeIndex, gulpOutputFileDescriptor):
        mode1 = np.zeros((self.numModes,2))
        mode2 = np.zeros((self.numModes,2))
        mode3 = np.zeros((self.numModes,2))
#        for i in range(self.numAtoms):
#            for j in range(3):
        i=0
        while True:
            line = gulpOutputFileDescriptor.readline()
            if line=="\n": # this kicks us out when we get to the end of the block
                break
            vals = (line.split())[2:]
            #print vals
            mode1[i][:] = np.array(vals[0:2])
            mode2[i][:] = np.array(vals[2:4])
            mode3[i][:] = np.array(vals[4:6])
            i += 1
#        mode1 = mode1.reshape(self.numAtoms,3,2)
#        mode2 = mode2.reshape(self.numAtoms,3,2)
#        mode3 = mode3.reshape(self.numAtoms,3,2)
        return [mode1,mode2,mode3]
    
    def _getComplexVecs(self, kpointIndex, modeIndex, gulpOutput):
        mode1=np.zeros((self.numAtoms*3),dtype=complex)
        mode2=np.zeros((self.numAtoms*3),dtype=complex)
        mode3=np.zeros((self.numAtoms*3),dtype=complex)
#        for i in range(self.numAtoms):
#            for j in range(3):
        i=0
        while True:
            line = gulpOutput.readline()
            if line=="\n": # this kicks us out when we get to the end of the block
                break
            vals = (line.split())[2:]
            #print vals
            operand1 = self._assignOperand(vals[1])
            operand3 = self._assignOperand(vals[3])
            operand5 = self._assignOperand(vals[5])
            #print vals, operand1
            mode1[i] = complex(vals[0]+operand1+vals[1]+'j')
            mode2[i] = complex(vals[2]+operand3+vals[3]+'j')
            mode3[i] = complex(vals[4]+operand5+vals[5]+'j')
            i += 1
        mode1 = mode1.reshape(self.numAtoms,3).tolist()
        mode2 = mode2.reshape(self.numAtoms,3).tolist()
        mode3 = mode3.reshape(self.numAtoms,3).tolist()
        return [mode1, mode2, mode3]
        
    def writeComplexVecs(self, kpointIndex, modeIndex, gulpOutputFileDescriptor):
        mode1,mode2,mode3 = self._getComplexVecs(kpointIndex, modeIndex, gulpOutputFileDescriptor)
        self.polWrite.writeVec(kpointIndex, modeIndex, mode1)
        self.polWrite.writeVec(kpointIndex, modeIndex+1, mode2)
        self.polWrite.writeVec(kpointIndex, modeIndex+2, mode3)
        
    def _assignOperand(self, num):
        if num[0] in '0123456789':
            return '+'
        elif num[0]=='-':
            return ''
        else:
            sys.stderr.write('unknown operator')
            sys.exit(2)
        
    def getGammaPtEigenvaluesAndEigenvectors(self):
        '''returns eigenvalues and vectors when kpt is 0,0,0'''
        gulpOutput = urllib.urlopen(self.gulpOutputFile)               
        self.eigs=[]
        self.vecs=[]
        kpointIndex=0
        modeIndex=0
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                break
            if 'Frequency' in line:
                #print frequencyLine.parseString(line)
                #if frequencyLine.parseString(line):
                space_re='[ \t]+'
                float_re='[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
                if re.search('Frequency' + space_re + float_re + space_re + float_re + 
                             space_re + float_re + space_re + float_re + space_re + float_re + space_re + float_re, line):
                    self.eigs += map(lambda x: float(x),(line.split())[1:])
                #move through the 6 intervening lines between frequencies and vecs
                for i in range(6):  
                    gulpOutput.readline()
                self.getGammaPtVecs(kpointIndex,modeIndex,gulpOutput)
                modeIndex+=6
                print 'parser found kpoint, mode',kpointIndex,modeIndex
#                self.eigs.append(eig)
            if modeIndex == self.numModes:
                kpointIndex += 1
                break
        gulpOutput.close()
        self.eigs = np.array(self.eigs)
        #turn these into energies
        if self.convertToEnergies:
            self.eigs = self.hbarTimesC*self.eigs
        #print self.eigs.shape
        #print (self.numKpoints,self.numModes)
        return self.eigs,self.vecs

    def getGammaPtEigenvalues(self):
        '''returns eigenvalues when kpt is 0,0,0'''
        import string
        gulpOutput = urllib.urlopen(self.gulpOutputFile)
        self.eigs=[]
        kpointIndex=0
        modeIndex=0
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                break
            if 'Frequency' in line:
                #print frequencyLine.parseString(line)
                #if frequencyLine.parseString(line):
                line = string.replace(line, '-', ' -')
                #have to be added to deal with negative frequencies without
                #space between them
                space_re='[ \t]+'
                float_re='[+-]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
                if re.search('Frequency' + space_re + float_re + space_re + float_re +
                             space_re + float_re + space_re + float_re + space_re + float_re + space_re + float_re, line):
                    self.eigs += map(lambda x: float(x),(line.split())[1:])
                #move through the 6 intervening lines between frequencies and vecs
                #print 'parser found kpoint, mode',kpointIndex,modeIndex
#                self.eigs.append(eig)
            if modeIndex == self.numModes:
                kpointIndex += 1
                break
        gulpOutput.close()
        self.eigs = np.array(self.eigs)
        #turn these into energies
        if self.convertToEnergies:
            self.eigs = self.hbarTimesC*self.eigs
        #print self.eigs.shape
        #print (self.numKpoints,self.numModes)
        return self.eigs
        
    def parseEigenvaluesEigenvectorsOneByOne(self):
        '''gets eigenvalues and vectors one by one and writes them to file--good for BIG eigenvectors'''
        
        gulpOutput = urllib.urlopen(self.gulpOutputFile)               
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file')
                sys.exit(2)
            if 'Number of k points for this configuration =' in line:
                self.numKpoints = int((line.split())[-1])
                break
        self.eigs=[]
        self.vecs=[]
        kpointIndex=0
        modeIndex=0
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                break
            if 'Frequency' in line:
                #print frequencyLine.parseString(line)
                #if frequencyLine.parseString(line):
                space_re='[ \t]+'
                float_re='[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
                if re.search('Frequency' + space_re + float_re + space_re + float_re + space_re + float_re, line):
                    self.eigs += map(lambda x: float(x),(line.split())[1:])
            elif 'Real    Imaginary   Real    Imaginary   Real    Imaginary' in line:
                gulpOutput.readline()
                self.getAndWriteVecs(kpointIndex,modeIndex,gulpOutput)
                modeIndex+=3
                print 'LargeEigenDataParser wrote kpoint, mode',kpointIndex,modeIndex
#                self.eigs.append(eig)
            if modeIndex==self.numModes:
                kpointIndex+=1
                modeIndex=0
        gulpOutput.close()
        self.eigs=np.array(self.eigs)
        #turn these into energies
        if self.convertToEnergies:
            self.eigs=self.hbarTimesC*self.eigs
        #print self.eigs.shape
        #print (self.numKpoints,self.numModes)
        #reshape according to the number of kpoints
        self.eigs=self.eigs.reshape((self.numKpoints, self.numModes))
        writeEs(self.eigs, self.EsFilename)   
  
    def getGammaPtVecs(self, kpointIndex, modeIndex, gulpOutput):
        mode1=np.zeros(self.numModes)
        mode2=np.zeros(self.numModes)
        mode3=np.zeros(self.numModes)
        mode4=np.zeros(self.numModes)
        mode5=np.zeros(self.numModes)
        mode6=np.zeros(self.numModes)
#        for i in range(self.numAtoms):
#            for j in range(3):
        vecs = []
        i=0
        while True:
            line = gulpOutput.readline()
            if line=="\n": # this kicks us out when we get to the end of the block
                break
            vals = (line.split())[2:]
            #print vals
            mode1[i] = vals[0]
            mode2[i] = vals[1]
            mode3[i] = vals[2]
            mode4[i] = vals[3]
            mode5[i] = vals[4]
            mode6[i] = vals[5]
            i+=1
            vecs += [mode1,mode2,mode3,mode4,mode5,mode6]
        return vecs
        
    def _parseKpoints(self):   
        """this function is necessary in output parser
         in order to know the specific
        kpoints used
        """
        def _getSpecificKpoints(gulpOutput):
            previousLineBlank=False
            while True:
                line = gulpOutput.readline()
                brillouinZonePart+=line
                if line=='\n': 
                    if previousLineBlank==True: break
                    else: previousLineBlank=True;continue
                else: previousLineBlank=False
            gulpOutput.close()
            #now get the kpoints:
            #kpointLines = OneOrMore(Group(Suppress(integer) + number + number + number + Suppress(number)))
            kpointLines = Group(integer + number + number + number + number)
            self._kpoints = []
            dataSource = kpointLines.scanString(brillouinZonePart)
            for rawData, dataStart, dataEnd in dataSource:
                data = rawData.asList()[0]
                self._kpoints.append(data[1:4])
            self.numKpoints = len(self._kpoints)
        def _getKpointMesh(line):
            self._kpointMesh = map(int, (line.split())[3:])
            
        #look through file:
        gulpOutput = urllib.urlopen(self.gulpOutputFile)
        brillouinZonePart=''
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file ')
                sys.exit(2)
            if 'Number of k points for this configuration' in line: 
                _getSpecificKpoints(gulpOutput)
                break
            if 'Brillouin zone sampling points' in line:
                _getSpecificKpoints(gulpOutput)
                break
            if 'Shrinking factors =' in line:
                _getKpointMesh()
                break

    @property
    def kpoints(self):
        if not hasattr(self, '_kpoints'):
            self._parseKpoints()
        return self._kpoints
    
    @property
    def numKpoints(self):
        if not hasattr(self, '_numKpoints'):
            self._parseKpoints()
        return self._numKpoints
    
    @property
    def kpointMesh(self):
        if not hasattr(self, '_kpointMesh'):
            self._parseKpoints()
        return self._kpointMesh
    
    def parseNumAtoms(self):
        gulpOutput = urllib.urlopen(self.gulpOutputFile)
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file')
                sys.exit(2)
            if 'Total number atoms/shells =' in line:
                break
        return int(line.split()[4])
    
    def _getLattice(self):
        if hasattr(self, '_lattice'):
            return self._lattice
        else:
            
            gulpOutput = urllib.urlopen(self.gulpOutputFile)
            while True:
                line = gulpOutput.readline()
                if not line: # this kicks us out when we get to the end of the file
                    break
                if 'Cartesian lattice vectors (Angstroms) :' in line:
                    break
            gulpOutput.readline()
            a = map(float, gulpOutput.readline().split())
            b = map(float, gulpOutput.readline().split())
            c = map(float, gulpOutput.readline().split())
            return [a, b, c]
    lattice = property(_getLattice)
    
    def _getReciprocalLattice(self):
        if hasattr(self, '_lattice'):
            return self._lattice
        else:
            from matter.Lattice import Lattice
            lattice = Lattice(base = self.lattice)
            return lattice.recbase
    reciprocal_lattice = property(_getReciprocalLattice)
    
    

        
#    def parseEigenvalues(self):
#        '''gets eigenvalues and writes them to file'''
#        
#        gulpOutput = urllib.urlopen(self.gulpOutputFile)
#        self.eigs=[]
#        kpointIndex=0
#        modeIndex=0
#        while True:
#            line = gulpOutput.readline()
#            if not line: # this kicks us out when we get to the end of the file
#                break
#            if 'Frequency' in line:
#                #print frequencyLine.parseString(line)
#                #if frequencyLine.parseString(line):
#                space_re='[ \t]+'
#                float_re='[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
#                if re.search('Frequency' + space_re + float_re + space_re + float_re + space_re + float_re, line):
#                    self.eigs += map(lambda x: float(x),(line.split())[1:])
#            if modeIndex==self.numModes:
#                kpointIndex+=1
#                modeIndex=0
#        gulpOutput.close()
#        self.eigs=np.array(self.eigs)
#        #turn these into energies
#        if self.convertToEnergies:
#            self.eigs=self.hbarTimesC*self.eigs
#        #print self.eigs.shape
#        #print (self.numKpoints,self.numModes)
#        #reshape according to the number of kpoints
#        self.eigs=self.eigs.reshape((self.numKpoints, self.numModes))
#        writeEs(self.eigs, self.EsFilename)  
            
if __name__=='__main__':
    pass
    #f=file('test.log','w')
    #print >>f, o.getEigsNVecsFast()
    #print readEigVecs()