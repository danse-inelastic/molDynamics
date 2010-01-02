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
        f = open('devDbPass.txt')
        passwd = f.read()
        f.close()
        db = connect(db ='postgres://vnf:'+passwd+'@vnf.caltech.edu/vnfa2b',echo=True)
        #db = connect(db ='postgres:///test',echo=1)
        db.autocommit(True)
        from dsaw.model.visitors.OrmManager import OrmManager
        orm = OrmManager(db, guid)
        
        from memd.gulp.GulpPotential import GulpPotential
        import os
#        ddsObj = dds()
#        ddsObj._init()
#        ddsObj.inventory.dataroot = os.path.abspath('.')
#        ddsObj._configure()
        #import sys
        #thisMod = sys.modules[__name__]
        #ddsObj.director = thisMod
        for potentialName in os.listdir('originalPotentials'):
            if potentialName[0]=='.': 
                continue
            f = open(os.path.join('originalPotentials', potentialName))
            librarycontent = f.read()
            f.close()
            
            try:
                record = orm.db.query(orm(GulpPotential)).filter_by(
                                    filename = potentialName).one()
                gulpPotential = orm.record2object(record)
            except Exception, err:
                print err
                print 'creating new potential'
                gulpPotential = GulpPotential()
            gulpPotential.filename = potentialName
            gulpPotential.potential_name = potentialName.split('.')[0]
            orm.save(gulpPotential)
            #put the potential in the potentials subdirectory
            libfile = self.dds.abspath(orm(gulpPotential), filename = potentialName)
            libDirectory,file = os.path.split(libfile)
            if not os.path.exists(libDirectory):
                try:
                    os.makedirs(libDirectory)
                except Exception, err:
                    raise RuntimeError, "unable to create directory %r. %s: %s" % (
                        self.path, err.__class__.__name__, err)
            open(libfile, 'w').write(librarycontent)
            #server = director.clerk.dereference(job.server)
            self.dds.remember(orm(gulpPotential), files=[potentialName])
            
        gulpPotential2 = orm.load(GulpPotential, id = orm(gulpPotential).id)
        print gulpPotential2.potential_name
        
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

#db.destroyAllTables()

if __name__=='__main__':
    app = dummy()
    app.run()