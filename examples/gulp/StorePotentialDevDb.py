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

from memd.gulp.GulpPotential import GulpPotential
from vnfb.components import dds
#gulpPotential = GulpPotential()
#gulpPotential.potential_name = 'first'
#orm.save(gulpPotential)
import os
for potentialName in os.listdir('originalPotentials'):
    if potentialName[0]=='.': continue
    f = file(os.path.join('originalPotentials',potentialName))
    librarycontent = f.read()
    ddsObj = dds()
    
    potential_filename = potentialName
    try:
#        gulpPotential = director.clerk.getRecordByID(GulpPotential, self.inventory.potential_name, 
#            associatedDataFileToVerify = self.inventory.potential_filename, director=director)
        1/0
        gulpPotential = orm.load(GulpPotential, id = '1')
    except:
        # if it doesn't exist, create a new one from this entry
        #gulpPotential = director.clerk.newDbObject(GulpPotential, id = self.inventory.potential_name)
        gulpPotential = GulpPotential()
        gulpPotential.filename = potential_filename
        orm.save(gulpPotential)
        
        #put the potential in the potentials subdirectory
        libfile = ddsObj.abspath(gulpPotential, filename = potential_filename)
        libDirectory,file = os.path.split(libfile)
        if not os.path.exists(libDirectory):
            try:
                os.makedirs(libDirectory)
            except Exception, err:
                raise RuntimeError, "unable to create directory %r. %s: %s" % (
                    self.path, err.__class__.__name__, err)
        open(libfile, 'w').write(librarycontent)
        #server = director.clerk.dereference(job.server)
        ddsObj.remember(gulpPotential, files=[potential_filename])
        break
    
    


gulpPotential2 = orm.load(GulpPotential, id = orm(gulpPotential).id)
print gulpPotential2.potential_name

#db.destroyAllTables()

