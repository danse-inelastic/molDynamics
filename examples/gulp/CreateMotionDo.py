#perform a motion dos calculation
base = 'graphiteShort'

rawTraject = base+'.his'

ncFile = base+'.nc'

cmd = 'postProcessGulp.py --historyFile='+rawTraject+' --ncFile='+ncFile
#temp sub for job submission
import os
os.system(cmd)

import os
curDir = os.path.abspath('.')
ncFilePath = os.path.join(curDir,ncFile)
from vsat.Motion import Motion
motion = Motion(trajectoryPath=ncFilePath)

#optional: insert Motion in db
#from dsaw.db import connect
#db = connect(db ='postgres:///test', echo=True)
#db = connect(db ='postgres:///vnfa2b', echo=True)
#db = connect(db ='postgres://linjiao:4OdACm#@localhost/vnfa2b', echo=True)
#db.autocommit(True)
#from dsaw.model.visitors.OrmManager import OrmManager
#_id = 0
#def guid():
#    global _id
#    _id += 1
#    return str(_id)
#orm = OrmManager(db, guid)
#orm.save(motion)

#optional
#db.destroyAllTables()
