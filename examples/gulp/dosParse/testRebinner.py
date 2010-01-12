import pylab as p
from rawGulpInvcmDosToMeVDoses import gulpDOSFile2TwoColumnAsciis
totDos,h2Dos = gulpDOSFile2TwoColumnAsciis('phon6x3FineMeshVecsGamma.dens')

# get the hydrogen dos
fp = file(h2Dos)
lines=fp.readlines()
xS=[];yS=[]
for line in lines:
    if '#' in line[0]: continue
    data = line.split()
    if data == []: continue
    xT,yT=map(float, data)
    xS.append(xT);yS.append(yT)
    
# rebin
from scipy.stats.stats import histogram, histogram2
lim = 350
#h,smallest,binWidth,junk = histogram(yS[:lim],numbins = 100)

xData = xS[:lim]
yData = yS[:lim]
numBins = 70
# first divide the x-axis into the bins required
class Bin:
    
    def getNumPts(self):
        return len(self.xPts)
    
    def getMidpoint(self):
        # assume the spacing between all xPoints is uniform
        xPtSpacing = self.xPts[1] - self.xPts[0]
        # then assume the y-axis values occur between the x-axis value it is paired with and the 
        # next x-axis value (that its "neighbor" is paired with)
        end = self.xPts[-1] + xPtSpacing
        self.spacing = end - self.xPts[0]
        return self.xPts[0] + self.spacing/2 
    
    def __init__(self, maxPts):
        self.maxPts = maxPts
        self.value = 0.0
        self.xPts = []
        self.spacing = 0.0

import math
leftOverPts, numXdataInBin = math.modf(len(xData)/numBins)
bins=[]
currentBin = Bin(numXdataInBin)
for xPt,yPt in zip(xData,yData):
    if currentBin.getNumPts() >= numXdataInBin:
        bins.append(currentBin)
        currentBin = Bin(numXdataInBin)
    currentBin.xPts.append(xPt)
    # then add together all the y axis values that fall within the new bin
    currentBin.value += yPt

# but when you plot, plot the y-axis value not at the x-axis pair, but at the midpoint between the x-axis pair
# and the one up from it.  Assume there is an additional x-axis point at the end with the same spacing as all the others.
newXData = [bin.getMidpoint() for bin in bins]
newYData = [bin.value for bin in bins]
    
#plot on matplotlib
p.subplot(211)
p.plot(xData,yData)
p.subplot(212)
p.plot(newXData, newYData)

#axis([0, 60, 0, 0.001])
#legend(('expanded graphite only','first spot on the graphite/c60 sample','second spot on the graphite/c60 sample'))
#xlabel('wave number (cm^-1)')
#ylabel('signal (arbitrary units)')
#title('raman spectrum from other spectrometer')
p.show()

## next plot experimental resolution
#fp = file(h2dos)
#lines=fp.readlines()
#xS=[];yS=[]
#for line in lines:
#    xT,yT=map(float, line.split())
#    xS.append(xT);yS.append(yT)
##plot on matplotlib
#plot(xS, yS)
##axis([0, 60, 0, 0.001])
##legend(('expanded graphite only','first spot on the graphite/c60 sample','second spot on the graphite/c60 sample'))
##xlabel('wave number (cm^-1)')
##ylabel('signal (arbitrary units)')
##title('raman spectrum from other spectrometer')
#show()

# next plot the convolution of first by second

#pl.savefig('/home/brandon/tex/graphiteKH2/msdNoK.png')
#pl.savefig('msdNoK.png')
