from pyparsing import *
import pickle
import numpy as np
from os import linesep
#import scipy.io
from Polarizations import write as writeEigVecs

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

eigAndVec = Suppress(Literal("Frequency")) + threeNums + \
  Suppress(Literal("Real    Imaginary   Real    Imaginary   Real    Imaginary")) + \
  OneOrMore(vecLine)

eigsAndVecs = OneOrMore(eigAndVec)



class OutputParser:
    
    def __init__(self,gulpOutputFile,inventory=''):
        
        # because output file may be quite large, we must parse only the parts we want and 
        # immediately extract them and put them in the desired return format
        
        # perhaps the best way to do this for now is to parse the file each time for each quantity 
        # you want since gulp output files tend to be free of unnecessary clutter

        # so eventually take the inventory and decide which values have been set and look for them (or have an object 
        # which has this information encoded)
        
        self.gulpOutputFile=gulpOutputFile
        #temp=file(inventory.sample.i.atomicStructure.i.xyzFile.i.inputFile)
        self.numAtoms=124#int(temp.readline())
        self.modes=3*self.numAtoms

    def getEigsNVecsFast(self):
        '''gets eigenvalues and vectors fast'''
        gulpOutput = file(self.gulpOutputFile)
        eigsOutput = file('eigs.out','w')
        self.eigs=[]
        self.vecs=[]
        while True:
            line = gulpOutput.readline()
            if not line:
                break
            if 'Frequency' in line:
                self.eigs=self.eigs+(line.split())[1:]
            elif 'Real    Imaginary   Real    Imaginary   Real    Imaginary' in line:
                gulpOutput.readline()
                self.getVecs(gulpOutput)
        gulpOutput.close()
        return self.eigs,self.vecs
                
    def getVecs(self,gulpOutput):
        mode1=[]
        mode2=[]
        mode3=[]
        for i in range(self.numAtoms):
            mode1=mode1 + (gulpOutput.readline().split())[2:]
            mode2=mode2 + (gulpOutput.readline().split())[2:]
            mode3=mode3 + (gulpOutput.readline().split())[2:]
        self.vecs.append(mode1)
        self.vecs.append(mode2)
        self.vecs.append(mode3)
        writeEigVecs
        
            

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
    
    
#        try:
#            for line in f:
#                if 'Frequency' in line:
#                    
#                    
#        finally:
#            f.close()
            
if __name__=='__main__':
    #o=OutputParser('/home/jbk/gulp3.0/newkc24PhononOpt/phon6x3FineMeshVecs.gout')
    o=OutputParser('/home/jbk/gulp3.0/kc24PhononsOpt/phonSmallFineMesh.gout')
    #o=OutputParser('/home/jbk/gulp3.0/kc24PhononsOpt/test.out')
    #print o.getEigenvectors()
    f=file('test.log','w')
    print >>f, o.getEigsNVecsFast()