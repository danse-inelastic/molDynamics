import os
import numpy as n

def newDos():
    return ['',[]]

def getGulpDoses(gulpFileName, format='tuple'):
    path,gulpfile = os.path.split(gulpFileName)
    datafileBase,ext = os.path.splitext(gulpfile)
    #os.chdir(path)
    #print os.path.abspath(os.path.curdir)
    f = file(gulpFileName)
    
    # split the DOS's up by comments (this is the general gulp method)
    # and name the new file from a hash of the Dos name
    currentDos = None
    allDos = []
    for line in f.readlines():
        if "#" in line:
            if currentDos is None:  # are we just starting out?
                currentDos=newDos()
            elif len(currentDos[1])>0:  # did we just run into a new dos?  if so store the old and reinitialize
                allDos.append(currentDos)
                currentDos = newDos()
            comments = currentDos[0]
            comments += line
            currentDos[0] = comments
        else:
            coord,g = line.split()
            currentDos[1].append((float(coord)*0.124, float(g)))
    allDos.append(currentDos)  # append that last dos
        
    if 'files' in format:
        outfiles = []
        for dos in allDos:
            comments = dos[0].split('#')
            dosIdentifier = comments[1].strip().split() # get the second one because the first item is '', then strip white space on outside and split
            outfile = 'meV_'+datafileBase+'_'+''.join(dosIdentifier)+'.txt'
            outfiles.append(outfile)
            fout=file(outfile,'w')
            print >>fout, dos[0]
            for line in dos[1]:
                print >>fout, line[0], line[1]
        return outfiles
    else:
        newDoses = []
        for dos in allDos:
            data = n.array(dos[1])
            data = data.transpose()
            newDoses.append([dos[0],data.tolist()])
        return newDoses
        

# first divide the x-axis into the bins required
class Bin:
    
    def getNumPts(self):
        return len(self.xPts)
    
    def getMidpoint(self):
        return self.xPts[0] + self.spacing/2 
    
    def __init__(self, maxPts):
        self.maxPts = maxPts
        self.value = 0.0
        self.xPts = []
        self.spacing = 0.0
        
#def getGulpDos(gulpDosFile):
#    allDoses = gulpDOSFile2TwoColumnAsciis(gulpDosFile)
#    # only get the hydrogen dos for now
#    fp = file(allDoses[-1])
#    lines=fp.readlines()
#    xS=[];yS=[]
#    for line in lines:
#        if '#' in line[0]: continue
#        data = line.split()
#        if data == []: continue
#        xT,yT=map(float, data)
#        xS.append(xT);yS.append(yT)
#    return xS,yS

def getGulpDosRebinned(filename, numBins = 70, cutoffOfDosData = None, format = 'columns'):
    #from multiphonon.DosPlottingUtils import getGulpDos
    data = getGulpDoses(filename)
    # need to generalize this next line so it plots *all* doses (as recorded in GulpSimulation)
    comment,dosData = data[-1]
    (xS,yS) = dosData
    #h,smallest,binWidth,junk = histogram(yS[:lim],numbins = 100)
    if cutoffOfDosData:
        xData = xS[:cutoffOfDosData]
        yData = yS[:cutoffOfDosData]
    else:
        xData = xS
        yData = yS
    
    #from multiphonon.DosPlottingUtils import Bin
    import math
    leftOverPts, numXdataInBin = math.modf(len(xData)/numBins)
    bins=[]
    currentBin = Bin(int(numXdataInBin))
    for xPt,yPt in zip(xData,yData):
        if currentBin.getNumPts() >= numXdataInBin:
            currentBin.spacing = xPt - currentBin.xPts[0]
            bins.append(currentBin)
            currentBin = Bin(int(numXdataInBin))
        currentBin.xPts.append(xPt)
        # then add together all the y axis values that fall within the new bin
        currentBin.value += yPt
    
    # but when you plot, plot the y-axis value not at the x-axis pair, but at the midpoint between the x-axis pair
    # and the one up from it.  Assume there is an additional x-axis point at the end with the same spacing as all the others.
    newXData = [bin.getMidpoint() for bin in bins]
    newYData = [bin.value for bin in bins]
    columnData = [newXData,newYData]
    if 'columns' in format:
        return columnData
    if 'rows' in format:
        data = n.array(columnData)
        data = data.transpose()
        rowData = data.tolist()
        return rowData
