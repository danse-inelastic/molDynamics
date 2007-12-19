from pyparsing import *
import pickle
import numpy as np
from os import linesep
import re
#import scipy.io
from idf.Polarizations import write as writeEigVecs
from idf.Polarizations import read as readEigVecs

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

frequencyLine = Suppress(Literal("Frequency")) + threeNums

#kpointLines = OneOrMore(Group(Suppress(integer) + number + number + number + Suppress(number)))
kpointLines = Group(integer + number + number + number + number)

eigAndVec = frequencyLine + \
  Suppress(Literal("Real    Imaginary   Real    Imaginary   Real    Imaginary")) + \
  OneOrMore(vecLine)

eigsAndVecs = OneOrMore(eigAndVec)

class EigenDataParser:
    
    def __init__(self,gulpOutputFile,inventory=''):
        
        # because output file may be quite large, we must parse only the parts we want and 
        # immediately extract them and put them in the desired return format
        
        # perhaps the best way to do this for now is to parse the file each time for each quantity 
        # you want since gulp output files tend to be free of unnecessary clutter

        # so eventually take the inventory and decide which values have been set and look for them (or have an object 
        # which has this information encoded)
        
        self.gulpOutputFile=gulpOutputFile
        #temp=file(inventory.sample.i.atomicStructure.i.xyzFile.i.inputFile)
#        self.numAtoms=124#int(temp.readline())
#        self.numModes=3*self.numAtoms
        self.numAtoms=1116#int(temp.readline())
        self.numModes=3*self.numAtoms
        self.numKpoints=0
        
    def getEigsOneByOne(self,outputFile="Polarizations.dat"):
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
        self.eigs=[]#np.zeros(self.numKpoints)
        self.vecs=[]#np.zeros(self.numKpoints)
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
                self.getVecs(gulpOutput)
#                self.eigs.append(eig)
        gulpOutput.close()
        #reshape according to the number of kpoints
        self.eigs=np.array(self.eigs)
        #print self.eigs.shape
        #print (self.numKpoints,self.numModes)
        self.eigs.reshape((self.numKpoints,self.numModes))
        self.vecs=np.array(self.vecs)
        #print self.vecs.shape
        #print (self.numKpoints,self.numModes,self.numAtoms,3)
        self.vecs=self.vecs.reshape((self.numKpoints,self.numModes,self.numAtoms,3))
        writeEigVecs(self.vecs,outputFile)
        return       

    def getAndWriteVecs(self,gulpOutput):
        mode1=np.zeros((self.numAtoms,3),dtype=complex)
        mode2=np.zeros((self.numAtoms,3),dtype=complex)
        mode3=np.zeros((self.numAtoms,3),dtype=complex)
        def assignOperand(num):
            if num[0] in '0123456789':
                return '+'
            elif num[0]=='-':
                return ''
            else:
                sys.stderr.write('unknown operator')
                sys.exit(2)
        for i in range(self.numAtoms):
            for j in range(3):
                vals = (gulpOutput.readline().split())[2:]
                operand1=assignOperand(vals[1])
                operand3=assignOperand(vals[3])
                operand5=assignOperand(vals[5])
                #print vals, operand1
                mode1[i][j]=complex(vals[0]+operand1+vals[1]+'j')
                mode2[i][j]=complex(vals[2]+operand3+vals[3]+'j')
                mode3[i][j]=complex(vals[4]+operand5+vals[5]+'j')
        self.vecs.append(mode1)
        self.vecs.append(mode2)
        self.vecs.append(mode3)
#    def writeEigVecsToFile(self):
#        writeEigVecs

    def getEigsNVecsFast(self,outputFile="Polarizations.dat"):
        '''gets eigenvalues and vectors fast'''
        gulpOutput = file(self.gulpOutputFile)
        while True:
            line = gulpOutput.readline()
            if not line: # this kicks us out when we get to the end of the file
                sys.stderr.write('no kpoints in this output file')
                sys.exit(2)
            if 'Number of k points for this configuration =' in line:
                self.numKpoints=int((line.split())[-1])
                break
        self.eigs=[]#np.zeros(self.numKpoints)
        self.vecs=[]#np.zeros(self.numKpoints)
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
                self.getVecs(gulpOutput)
#                self.eigs.append(eig)
        gulpOutput.close()
        #reshape according to the number of kpoints
        self.eigs=np.array(self.eigs)
        #print self.eigs.shape
        #print (self.numKpoints,self.numModes)
        self.eigs.reshape((self.numKpoints,self.numModes))
        self.vecs=np.array(self.vecs)
        #print self.vecs.shape
        #print (self.numKpoints,self.numModes,self.numAtoms,3)
        self.vecs=self.vecs.reshape((self.numKpoints,self.numModes,self.numAtoms,3))
        writeEigVecs(self.vecs,outputFile)
        return
                
    def getVecs(self,gulpOutput):
        mode1=np.zeros((self.numAtoms,3),dtype=complex)
        mode2=np.zeros((self.numAtoms,3),dtype=complex)
        mode3=np.zeros((self.numAtoms,3),dtype=complex)
        def assignOperand(num):
            if num[0] in '0123456789':
                return '+'
            elif num[0]=='-':
                return ''
            else:
                sys.stderr.write('unknown operator')
                sys.exit(2)
        for i in range(self.numAtoms):
            for j in range(3):
                vals = (gulpOutput.readline().split())[2:]
                operand1=assignOperand(vals[1])
                operand3=assignOperand(vals[3])
                operand5=assignOperand(vals[5])
                #print vals, operand1
                mode1[i][j]=complex(vals[0]+operand1+vals[1]+'j')
                mode2[i][j]=complex(vals[2]+operand3+vals[3]+'j')
                mode3[i][j]=complex(vals[4]+operand5+vals[5]+'j')
        self.vecs.append(mode1)
        self.vecs.append(mode2)
        self.vecs.append(mode3)
#    def writeEigVecsToFile(self):
#        writeEigVecs
        
    def getKpoints(self):
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
        return self.kpoints 
        
#------------------------------------------------------------deprecated        
    def readChunk(self, gulpOutput, chunkSize=1000):
        '''reads a chunk of the file, but always breaks at two or more consecutive blank lines'''
        previousLineBlank=False
        linecount=0
        lines=''
        while True:
            line = gulpOutput.readline()
    #    for line in gulpOutput:
            linecount+=1
            lines+=line
            if linecount<chunkSize: continue
            else:
                if line=='\n': 
                    if previousLineBlank==True: break
                    else: previousLineBlank=True;continue
                else: previousLineBlank=False
        return lines
            
#------------------------------------------------------------deprecated 
    def getEigenvectors(self):
        '''get the eigenvalues and eigenvectors and output them in Max's format'''
        eigsVecsList = []
        f=file(self.outputFile)
        log=file('log','w')
        try:
            while True:
                fileChunk=self.readChunk(f)
                print >>log, fileChunk
                dataSource=eigsAndVecs.scanString(fileChunk)
        
                for data, dataStart, dataEnd in dataSource:
                    eigsVecsList.append(data.asList())   
                print eigsVecsList
        except:
            pass
        return eigsVecsList
    
        # below is code to look for a double blank in gulp's output
#            previousLineBlank=False
#            linecount=0
#            lines=''
#            linecount+=1
#            lines+=line
#            if linecount<chunkSize: continue
#            else:
#                if line=='\n': 
#                    if previousLineBlank==True: break
#                    else: previousLineBlank=True;continue
#                else: previousLineBlank=False
#        return lines
    
            
if __name__=='__main__':
    o=OutputParser('/home/jbk/gulp3.0/newkc24PhononOpt/phon6x3FineMeshVecs.gout')
    #o=OutputParser('/home/jbk/gulp3.0/kc24PhononsOpt/phonSmallFineMesh.gout')
    #o=OutputParser('/home/jbk/gulp3.0/kc24PhononsOpt/test.out')
    #o.getEigsNVecsFast(outputFile="PolarizationsTest.dat")
    #o.getKpoints()
    o.getEigsOneByOne(outputFile="/home/jbk/DANSE/MolDyn/molDynamics/tests/gulpTests/parsingTests/PolarizationsTest.dat")
    #f=file('test.log','w')
    #print >>f, o.getEigsNVecsFast()
    #print readEigVecs()