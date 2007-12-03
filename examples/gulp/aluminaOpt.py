#script to optimize the crystal structure of (NH2)2CO (urea)
from sample.Sample import Sample
from molDynamics.gulp.forcefields.AluminaForcefield import AluminaForcefield  
from applications.MdApp import MdApp
from UnitCell import UnitCell
# set up the sample with atoms, periodicity, atomic interactions
sample = Sample() 
unitCell = UnitCell()
unitCell.i.a = '2.380100 1.374151 4.331100'
unitCell.i.b = '-2.380100 1.374151 4.331100'
unitCell.i.c = '0.000000 -2.748303 4.331100'
 
sample.i.atoms = '''[['C', 0.00000000, 0.50000000, 0.32600000], 
['C', 0.49999920, 0.00000000, 0.61502595], 
['O', 0.00000000, 0.49999998, 0.58816619], 
['O', 0.50000040, -0.00000039, 0.35285659], 
['N', 0.14293176, 0.64293184, 0.18101006], 
['N', 0.85706814, 0.35706821, 0.18101006], 
['N', 0.64293288, 0.85706713, 0.76001372], 
['N', 0.35706811, 0.14293188, 0.76001345], 
['H', 0.26167656, 0.76167659, 0.27731462], 
['H', 0.73832344, 0.23832347, 0.27731458], 
['H', 0.76167757, 0.73832243, 0.66370978], 
['H', 0.23832195, 0.26167805, 0.66370971], 
['H', 0.13785881, 0.63785890, 0.96043229], 
['H', 0.86214114, 0.36214121, 0.96043228], 
['H', 0.63785790, 0.86214210, -0.01940859], 
['H', 0.36214109, 0.13785891, -0.01940832]]'''
sample.i.partialCharges = "{'C':0.380000, 'O':-0.380000, 'N':-0.830000, 'H':0.415000}"
sample.i.initialTemp = 300.0
sample.i.forcefield = AluminaForcefield()
    
# invoke the application and set its inventory
app = MdApp()
g = app.i.mdEngine
g.i.sample = sample
g.i.runType = 'optimize'
g.i.coordinateFormat = 'fractional'
g.i.optimizeCoordinates = True
g.i.optimizeCell = True
g.i.constantPressureOptimize = True
g.i.dispersionInRecipSpace = True
g.i.computeMaterialProperties = True
g.i.identifyMolecules = True
g.i.engineExecutablePath = '/home/brandon/gulp3.0/practice/gulp'
g.i.inputDeck = 'ureaOpt.gin'
g.i.trajectoryFilename = 'ureaOpt.xyz'
g.i.logFilename = 'ureaOpt.log'
app.run()

print g.getFinalConfiguration()
print 
