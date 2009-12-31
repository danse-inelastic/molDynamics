_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)

#connect to db
from dsaw.db import connect
f = file('devDbPass.txt')
passwd = f.read()
db = connect(db ='postgres://vnf:'+passwd+'@vnf.caltech.edu/vnfa2b')
#db = connect(db ='postgres:///test',echo=1)
db.autocommit(True)
from dsaw.model.visitors.OrmManager import OrmManager
orm = OrmManager(db, guid)


#create settings
from memd.gulp.GulpSettings import GulpSettings
gulpSettings = GulpSettings(runtype='md')
gulpSettings.runtype='phonons'
from matter.Structure import Structure
s = orm.load(Structure, '3W4G7NUM')
gulpSettings.structure = s

#store settings in db
orm.save(gulpSettings)

#retrieve the d.o.
gulpSettings2 = orm.load(GulpSettings, id = orm(gulpSettings).id)
print gulpSettings2.runtype

#db.destroyAllTables()

