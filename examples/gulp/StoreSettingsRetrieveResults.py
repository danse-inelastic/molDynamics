_id = 0
def guid():
    global _id
    _id += 1
    return str(_id)

#Create settings
###########################
from memd.gulp.GulpSettings import GulpSettings
gulpSettings = GulpSettings(runtype='md')
gulpSettings.runtype='phonons'

#Store settings in db
####################

from dsaw.db import connect
#db = connect(db ='postgres://linjiao:4OdACm#@localhost/vnfa2b')
db = connect(db ='postgres:///test')
db.autocommit(True)
from dsaw.model.visitors.OrmManager import OrmManager
orm = OrmManager(db, guid)
orm.save(gulpSettings)

# retrieve the d.o.
###################
gulpSettings2 = orm.load(GulpSettings, id=orm(gulpSettings).id)
print gulpSettings2.runtype

db.destroyAllTables()

