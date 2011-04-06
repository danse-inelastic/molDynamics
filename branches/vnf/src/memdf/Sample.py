#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from os import linesep
class Sample(object):
    '''This is a container class which holds atoms, external conditions, 
unit cells, or anything else pertaining to the sample.'''
    xyzFile=''
    temperature=0.0
    pressure=0.0

    def __init__(self):
        self.atomStrings = None
        self.ucVecs = None
        
    def initializeFromFile(self):
        try:
            f=file(self.i.inputFile)
        except:
            print "cannot open xyz file"
            raise
        self.atomStrings = f.readlines()
        try:
            ax,ay,az,bx,by,bz,cx,cy,cz = self.atomStrings[1].split()
            self.ucVecs = [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]
        except:
            ax,ay,az,bx,by,bz,cx,cy,cz = 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0
            self.ucVecs = [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]
        return ax,ay,az,bx,by,bz,cx,cy,cz

    def gulpFormatUcNAtoms(self,runType):
#        try:
#            f=file(self.i.inputFile)
#        except:
#            print "cannot open xyz file"
#            raise
#        lines=f.readlines()
#        ax,ay,az,bx,by,bz,cx,cy,cz = self.ucVecs
        ax,ay,az,bx,by,bz,cx,cy,cz = self.initializeFromFile()
        text='vectors'+linesep + ax+' '+ay+' '+az + linesep + bx+' '+by+' '+bz+linesep + cx+' '+cy+' '+cz+linesep
        if runType.runTypeIdentifier=='optimize':
            if runType.i.optimizeCell:
                #remove the last linesep and add the optimize flags
                text=text[:-1]+' 1 1 1 1 1 1'+linesep
        text+='cartesian'+linesep
        for line in self.atomStrings[2:]:
            text+=line
        text+=linesep
        return text
    
    def getAtomsAsStrings(self):
        if not self.atomStrings:
            self.initializeFromFile()
        return self.atomStrings[2:]
    
    def getCellVectors(self):
        if not self.ucVecs:
            self.initializeFromFile()
        return self.ucVecs
    