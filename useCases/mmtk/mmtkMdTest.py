#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# list of inputs:
inputs = {
'engine':'mmtk',
'engine.sampleBuilder.temp':300.0,
'engine.sampleBuilder.atoms':[],
'engine.sampleBuilder.atomPositions':[],
'engine.sampleBuilder.lattice':(7.243, 9.310, 6.756, 90.0, 90.0, 90.0),
'engine.runType':'md',
'engine.forcefields':,
'engine.ensemble':'nve',
'engine.timestep':0.5,
'engine.equilibriumTime':0.005,
'engine.productionTime':0.4,   
          }
#f = file('runMd.sh')
#f.write(')

for key,val in inputs.iteritems():
    appCommand+' --'+key+'='+val
import os
os.system(appCommand)


md.i.sample = self.sample
md.i.runType = 'md'
md.i.forcefields = lennard
md.i.ensemble = 'nve'
md.i.timestep = 0.5
md.i.equilibrationTime = 0.005
md.i.productionTime = 0.4
md.integrate()














def main():


    from pyre.applications.ClientServer import ClientServer


    class IPAApp(ClientServer):


        class Inventory(ClientServer.Inventory):

            import pyre.inventory

            # the key used by the remote server
            key = pyre.inventory.str("key", default="deadbeef")

            # host where the journal server is located
            host = pyre.inventory.str("host", default="localhost")

            # port used by the remote server
            port = pyre.inventory.int("port", default=50000)
            
            # the name of the client session component
            clientName = pyre.inventory.str('client-name', default='ipa-session')
            

        def onServer(self):
            name = 'ipa'

            # turn on my channels so we can watch what happens
            import journal
            journal.info(name).activate()
            # journal.debug(name).activate()

            journal.info("user-manager").activate()
            # journal.debug("user-manager").activate()

            # build the registry settings
            registry = self.createRegistry()
            registry.name = 'root'
            node = registry.getNode(name)
            node.setProperty('port', self.port,  None)

            marshaller = node.getNode('marshaller')
            marshaller.setProperty('key', self.key, None)

            userManager = node.getNode('user-manager')
            userManager.setProperty('passwd', 'userdb.md5',  None)

            # instantiate the services
            import pyre.ipa
            service = pyre.ipa.service(name)
            service.weaver = self.weaver

            # configure it
            self.configureComponent(service, registry)

            # initialize it
            service.init()

            # client configuration
            registry = self.createRegistry()
            serviceRegistry = registry.getNode(self.clientName)
            service.generateClientConfiguration(serviceRegistry)

            stream = file(self.clientName + '.pml', 'w')
            document = self.weaver.render(registry)
            print >> stream, "\n".join(document)
            stream.close()

            # enter the indefinite loop waiting for requests
            service.serve()

            return


        def onClient(self):
            name = self.clientName

            import journal
            journal.info(name).activate()
            # journal.debug(name).activate()
            journal.info('pickler').activate()
            # journal.debug('pickler').activate()

            # instantiate the client
            import pyre.ipa
            client = pyre.ipa.session(name)

            # configure it
            self.configureComponent(client)

            # initialize it
            client.init()

            # get a ticket
            ticket = client.login("aivazis", "mga4demo")
            print "got ticket:", ticket

            # refresh it
            ticket = client.refresh("aivazis", ticket)
            print "got new ticket:", ticket

            # logout
            response = client.logout("aivazis", ticket)
            print "got:", response

            return


        def __init__(self, name):
            ClientServer.__init__(self, name)
            self.key = ''
            self.host = ''
            self.port = 0
            self.clientName = ''
            return


        def _configure(self):
            ClientServer._configure(self)
            self.key = self.inventory.key
            self.host = self.inventory.host
            self.port = self.inventory.port
            self.clientName = self.inventory.clientName
            return


    name = "ipaapp"

    import journal
    journal.info(name).activate()
    
    app = IPAApp(name)
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: ipa.py,v 1.1.1.1 2006-11-27 00:10:11 aivazis Exp $"

# End of file 
