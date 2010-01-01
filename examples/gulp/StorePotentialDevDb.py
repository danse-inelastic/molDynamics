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
#gulpPotential = GulpPotential()
#gulpPotential.potential_name = 'first'
#orm.save(gulpPotential)
import os
for potentialName in os.listdir('originalPotentials'):
    f = file(potentialName)
    f.read()
    
    
    gulpPotential = GulpPotential()
    baseName,ext = os.path.splitext(potentialName)
    gulpPotential.potential_name = baseName
    gulpPotential.filename = potentialName
    g
    orm.save(gulpPotential)

gulpPotential2 = orm.load(GulpPotential, id = orm(gulpPotential).id)
print gulpPotential2.potential_name

#db.destroyAllTables()

