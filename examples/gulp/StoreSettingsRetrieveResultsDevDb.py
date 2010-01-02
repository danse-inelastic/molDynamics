_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)

#connect to db
from dsaw.db import connect
f = file('devDbPass.txt')
passwd = f.read()
db = connect(db ='postgres://vnf:'+passwd+'@vnf.caltech.edu/vnfa2b',echo=True)
#db = connect(db ='postgres:///test',echo=1)
db.autocommit(True)
from dsaw.model.visitors.OrmManager import OrmManager
orm = OrmManager(db, guid)

#create settings
from memd.gulp.GulpSettings import GulpSettings
gulpSettings = GulpSettings(runtype='md')
gulpSettings.runtype='phonons'
#from matter.Structure import Structure
#from matter.orm.Structure import Structure
from vnfb.dom.AtomicStructure import Structure
s = orm.load(Structure, '3W4G7NUM')
gulpSettings.structure = s
from memd.gulp.GulpPotential import GulpPotential

p = orm.load(GulpPotential, '1')

gulpSettings.potential = p
#store settings in db
orm.save(gulpSettings)


        # these last few lines will eventually be taken care of by the orm
        #create data directory for the simulation if necessary
        datadir = director.dds.abspath(orm(gulpSettings))
        if not os.path.exists(datadir): os.makedirs(datadir)

        inputFilePath = director.dds.abspath(orm(gulpSettings), filename=GulpSettings.inputFile)
        open(inputFilePath, 'w').write(self.inventory.inputFileContents)
        
        #these lines should be executed right before the job is submitted
        #get the potential from the database
        potentialPath = director.dds.abspath(gulpPotential, filename=gulpPotential.filename)
        potentialContent = open(potentialPath).read()
        #write the potential in the simulation directory
        simulationPotential = director.dds.abspath(gulpSettings, filename=gulpPotential.filename)
        open(simulationPotential, 'w').write(potentialContent)      


#retrieve the d.o.
gulpSettings2 = orm.load(GulpSettings, id = orm(gulpSettings).id)
print gulpSettings2.runtype

#db.destroyAllTables()

