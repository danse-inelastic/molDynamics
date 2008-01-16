from pyparsing import *
import pickle
import numpy as np
from os import sep
import re, sys
#import scipy.io
from molDynamics.gulp.E import write as writeEs
from molDynamics.gulp.NetcdfPolarizationWrite import NetcdfPolarizationWrite

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

#kpointLines = OneOrMore(Group(Suppress(integer) + number + number + number + Suppress(number)))
kpointLines = Group(integer + number + number + number + number)

eigAndVec = frequencyLine + \
  Suppress(Literal("Real    Imaginary   Real    Imaginary   Real    Imaginary")) + \
  OneOrMore(vecLine)

eigsAndVecs = OneOrMore(eigAndVec)

class LargeEigenDataParser:
    
    hbarTimesC=6.58211899e-16*1e3*29.978*1e9#hbar eV*s * 1 meV/eV * c cm/s = hbarTimesC meV*cm
    
    def __init__(self, gulpOutputFile, inventory='',EsFilename="Es.dat", polarizationsFilename="Polarizations.nc"):
        # because output file may be quite large, we must parse only the parts we want and 
        # immediately extract them and put them in the desired return format
        
        # perhaps the best way to do this for now is to parse the file each time for each quantity 
        # you want since gulp output files tend to be free of unnecessary clutter

        # so eventually take the inventory and decide which values have been set and look for them (or have an object 
        # which has this information encoded)
        self.removeNegativeFrequencies=True # eventually put in a way to remove negative frequencies
        self.convertToEnergies=True
        self.gulpOutputFile=gulpOutputFile
        self.EsFilename=EsFilename
        #temp=file(inventory.sample.i.atomicStructure.i.xyzFile.i.inputFile)
        self.parseNumAtoms()
#        self.numAtoms=1116#int(temp.readline())
        self.numModes=3*self.numAtoms
        self.parseKpoints()
#        self.pWrite=PolarizationWrite(filename=polarizationsFilename, 
#                                numAtoms=self.numAtoms, numks=self.numKpoints)
        self.polWrite=NetcdfPolarizationWrite(filename=polarizationsFilename, 
                                numks=self.numKpoints, numAtoms=self.numAtoms)
        
    def parseEigsOneByOne(self):
        '''gets eigenvalues and vectors one by one and writes them to file--good for BIG eigenvectors'''
        
        gulpOutput = file(self.gulpOutputFile)
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file')
                sys.exit(2)
            if 'Number of k points for this configuration =' in line:
                self.numKpoints=int((line.split())[-1])
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
                print 'wrote kpoint, mode',kpointIndex,modeIndex
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

    def getAndWriteVecs(self, kpointIndex, modeIndex, gulpOutput):
        mode1=np.zeros((self.numModes,2))
        mode2=np.zeros((self.numModes,2))
        mode3=np.zeros((self.numModes,2))
        def assignOperand(num):
            if num[0] in '0123456789':
                return '+'
            elif num[0]=='-':
                return ''
            else:
                sys.stderr.write('unknown operator')
                sys.exit(2)
#        for i in range(self.numAtoms):
#            for j in range(3):
        i=0
        while True:
            line = gulpOutput.readline()
            if line=="\n": # this kicks us out when we get to the end of the block
                break
            vals = (line.split())[2:]
            #print vals
            mode1[i][:]=np.array(vals[0:2])
            mode2[i][:]=np.array(vals[2:4])
            mode3[i][:]=np.array(vals[4:6])
            i+=1
        mode1=mode1.reshape(self.numAtoms,3,2)
        mode2=mode2.reshape(self.numAtoms,3,2)
        mode3=mode3.reshape(self.numAtoms,3,2)
        #print 'mode1',mode1
        #sys.exit()
#        self.polWrite.writeVec(kpointIndex, modeIndex, mode1)
#        self.polWrite.writeVec(kpointIndex, modeIndex+1, mode2)
#        self.polWrite.writeVec(kpointIndex, modeIndex+2, mode3)
        self.polWrite.writeVec(mode1)
        self.polWrite.writeVec(mode2)
        self.polWrite.writeVec(mode3)

    def getAndWriteVecsAsComplex(self, kpointIndex, modeIndex, gulpOutput):
        mode1=np.zeros((self.numAtoms*3),dtype=complex)
        mode2=np.zeros((self.numAtoms*3),dtype=complex)
        mode3=np.zeros((self.numAtoms*3),dtype=complex)
        def assignOperand(num):
            if num[0] in '0123456789':
                return '+'
            elif num[0]=='-':
                return ''
            else:
                sys.stderr.write('unknown operator')
                sys.exit(2)
#        for i in range(self.numAtoms):
#            for j in range(3):
        i=0
        while True:
            line = gulpOutput.readline()
            if line=="\n": # this kicks us out when we get to the end of the block
                break
            vals = (line.split())[2:]
            #print vals
            operand1=assignOperand(vals[1])
            operand3=assignOperand(vals[3])
            operand5=assignOperand(vals[5])
            #print vals, operand1
            mode1[i]=complex(vals[0]+operand1+vals[1]+'j')
            mode2[i]=complex(vals[2]+operand3+vals[3]+'j')
            mode3[i]=complex(vals[4]+operand5+vals[5]+'j')
            i+=1
        mode1=mode1.reshape(self.numAtoms,3)
        mode2=mode2.reshape(self.numAtoms,3)
        mode3=mode3.reshape(self.numAtoms,3)
        self.polWrite.writeVec(kpointIndex, modeIndex, mode1)
        self.polWrite.writeVec(kpointIndex, modeIndex+1, mode2)
        self.polWrite.writeVec(kpointIndex, modeIndex+2, mode3)
        
    def parseKpoints(self):
        gulpOutput = file(self.gulpOutputFile)
        brillouinZonePart=''
        #first look for Brillouin zone sampling part of output file:
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file')
                sys.exit(2)
            if 'Brillouin zone sampling points :' in line:
                break
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
        self.kpoints = []
        dataSource=kpointLines.scanString(brillouinZonePart)
        for data, dataStart, dataEnd in dataSource:
            self.kpoints.append(data.asList())
        self.numKpoints=len(self.kpoints)
                 
    def getKpoints(self):
        return self.kpoints
    
    def parseNumAtoms(self):
        gulpOutput = file(self.gulpOutputFile)
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file')
                sys.exit(2)
            if 'Total number atoms/shells =' in line:
                break
        self.numAtoms=int(line.split()[4])

    
            
if __name__=='__main__':
    mdParsing="/home/jbk/DANSE/MolDyn/molDynamics/tests/gulpTests/parsingTests"
    #o=OutputParser('/home/jbk/gulp3.0/newkc24PhononOpt/phon6x3FineMeshVecs.gout')
    o=LargeEigenDataParser('/home/jbk/gulp3.0/kc24PhononsOpt/phonSmallFineMesh.gout',
        polarizationsFilename=mdParsing+sep+"PolarizationsTest.dat",
        EsFilename=mdParsing+sep+"Es.dat")
    #o=OutputParser('/home/jbk/gulp3.0/kc24PhononsOpt/test.out')
    #o.getEigsNVecsFast(outputFile="PolarizationsTest.dat")
    #o.getKpoints()
    o.parseEigsOneByOne()
    #f=file('test.log','w')
    #print >>f, o.getEigsNVecsFast()
    #print readEigVecs()