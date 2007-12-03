#script to optimize the crystal structure of (NH2)2CO (urea)
from sample.Sample import Sample
from molDynamics.gulp.TwoAtomPotential import TwoAtomPotential
from molDynamics.gulp.ThreeAtomPotential import ThreeAtomPotential
from molDynamics.gulp.FourAtomPotential import FourAtomPotential    
from applications.MdApp import MdApp
#from MdApp import MdApp
import danseGlob
from os import sep
# set up the sample with atoms, periodicity, atomic interactions
sample = Sample()  
sample.i.unitCell = '''[[5.550830, 0.0, 0.0], [0.0, 5.550830, 0.0], 
[0.0, 0.0, 4.695612]]'''
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

CAndOBond = TwoAtomPotential('C', 'O')
CAndOBond.assignInteraction('morseGulpEx10')
CAndOBond.i.interIntra = 'intra'

CAndNBond = TwoAtomPotential('C', 'N')
CAndNBond.assignInteraction('morseGulpEx10')
CAndNBond.i.interIntra = 'intra'

HAndNBond = TwoAtomPotential('H', 'N')
HAndNBond.assignInteraction('morseGulpEx10')
HAndNBond.i.interIntra = 'intra'

CAndO = TwoAtomPotential('C', 'O')
CAndO.assignInteraction('lennardGulpEx10')
CAndO.i.interIntra = 'inter'

CAndN = TwoAtomPotential('C', 'N')
CAndN.assignInteraction('lennardGulpEx10')
CAndN.i.interIntra = 'inter'

OAndO = TwoAtomPotential('O', 'O')
OAndO.assignInteraction('lennardGulpEx10')
OAndO.i.interIntra = 'inter'

NAndO = TwoAtomPotential('N', 'O')
NAndO.assignInteraction('lennardGulpEx10')
NAndO.i.interIntra = 'inter'

NAndN = TwoAtomPotential('N', 'N')
NAndN.assignInteraction('lennardGulpEx10')
NAndN.i.interIntra = 'inter'

CAndC = TwoAtomPotential('C', 'C')
CAndC.assignInteraction('lennardGulpEx10')  
CAndC.i.interIntra = 'inter'      

NAndCAndO = ThreeAtomPotential('N', 'C', 'O')
NAndCAndO.assignInteraction('threeBodyGulpEx10')    
 
HAndNAndC = ThreeAtomPotential('H', 'N', 'C')
HAndNAndC.assignInteraction('threeBodyGulpEx10') 
 
HAndNAndH = ThreeAtomPotential('H', 'N', 'H')
HAndNAndH.assignInteraction('threeBodyGulpEx10') 
               
NAndCAndN = ThreeAtomPotential('N', 'C', 'N')
NAndCAndN.assignInteraction('threeBodyGulpEx10') 
               
OAndCAndNAndH = FourAtomPotential('O', 'C', 'N', 'H')
OAndCAndNAndH.assignInteraction('torsionGulpEx10') 
               
NAndCAndNAndH = FourAtomPotential('N', 'C', 'N', 'H')
NAndCAndNAndH.assignInteraction('torsionGulpEx10') 
               
OAndCAndNAndN = FourAtomPotential('O', 'C', 'N', 'N')
OAndCAndNAndN.assignInteraction('torsionGulpEx10') 
                       
forcefields = [CAndOBond, CAndNBond, HAndNBond, CAndO, CAndN, OAndO, NAndO, NAndN, 
             CAndC, NAndCAndO, HAndNAndC, HAndNAndH, NAndCAndN, OAndCAndNAndH, 
             NAndCAndNAndH, OAndCAndNAndN]
sample.i.forcefields = forcefields
    
# invoke the application and set its inventory
app = MdApp()
print app.inventory.propertyNames()
#def emptymain(self): 
#    print self.i.mdEngine
#    return
#appmain = app.main
#app.__class__.main = emptymain
#app.run()
#app.main = appmain
g = app.i.mdEngine
g.i.sample = sample
g.i.runType = 'optimize'
g.i.coordinateFormat = 'fractional'
g.i.optimizeCoordinates = True
g.i.optimizeCell = True
g.i.constantPressureOptimize = True
g.i.dispersionInRecipSpace = True
g.i.computeMaterialProperties = True
g.i.executablePath = danseGlob.installDir+sep+'gulp/gulp3.0/practice/gulp'
g.i.inputDeck = 'ureaOpt.gin'
g.i.trajectoryFilename = 'ureaOpt.xyz'
g.i.logFilename = 'ureaOpt.log'
app.run()
