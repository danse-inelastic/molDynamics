#get motion from trajectory
execfile('GetDosFromMotion.py')

#insert MotionDosCalc in db
orm.save(mdc)

#optional
db.destroyAllTables()