
try:
    f = file('guid.dat')
    _id = int(f.read())
    f.close()
except:
    _id = 0
def guid():
    global _id
    _id += 1
    return str(_id)

# connect to current idd server
#import pyre.idd
##create an INET, STREAMing socket
#import socket
#s = socket.socket(
#    socket.AF_INET, socket.SOCK_STREAM)
##now connect to the web server on port 80 
## - the normal http port
#s.connect(("localhost", 80))
#pyre.idd.session


from pyre.applications.Script import Script as base
import os

class dummy(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        id = pyre.inventory.str('id')

        import vnfb.components
        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnfb.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        dds = pyre.inventory.facility(name="dds", factory=vnfb.components.dds)
        dds.meta['tip'] = "the component manages data files"

        csaccessor = pyre.inventory.facility(name='csaccessor', factory = vnf.components.ssher)
        csaccessor.meta['tip'] = 'computing server accessor'

        debug = pyre.inventory.bool(name='debug', default=False)

    def main(self):
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
        
        p = orm.load(GulpPotential, '41')
        
        gulpSettings.potential = p
        #store settings in db
        orm.save(gulpSettings)
        
        
        # these last few lines will eventually be taken care of by the orm
        #create data directory for the simulation if necessary
        datadir = self.dds.abspath(orm(gulpSettings))
        if not os.path.exists(datadir): os.makedirs(datadir)
        
        inputFileContents = 'energy/n'
        inputFilePath = self.dds.abspath(orm(gulpSettings), filename=GulpSettings.inputFile)
        open(inputFilePath, 'w').write(inputFileContents)
        
        #these lines should be executed right before the job is submitted
        #get the potential from the database
        gulpPotential = gulpSettings.potential
        potentialPath = self.dds.abspath(orm(gulpPotential), filename=gulpPotential.filename)
        potentialContent = open(potentialPath).read()
        #write the potential in the simulation directory
        simulationPotential = self.dds.abspath(orm(gulpSettings), filename=gulpPotential.filename)
        open(simulationPotential, 'w').write(potentialContent)      
        
        
        #retrieve the d.o.
        gulpSettings2 = orm.load(GulpSettings, id = orm(gulpSettings).id)
        print gulpSettings2.runtype
        
        #db.destroyAllTables()
        
        f = open('guid.dat','w')
        f.write(str(_id))
        f.close()

    def __init__(self, name='dummy'):
        super(dummy, self).__init__(name)
        return


    def _configure(self):
        super(dummy, self)._configure()

        self.debug = self.inventory.debug

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.dds = self.inventory.dds
        self.dds.director = self
        self.csaccessor = self.inventory.csaccessor
        return


    def _init(self):
        super(dummy, self)._init()

        # initialize table registry
#        import vnf.dom
#        vnf.dom.register_alltables()
        return
    
if __name__=='__main__':
    app = dummy()
    app.run()