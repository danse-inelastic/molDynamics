Science Tutorial: Switching computational engines
=================================================

.. .. index:: 

Let us demonstrate how to switch computational engines::

	class MdApp(Script):
	    '''Driver for the md engines in DANSE.'''
	    class Inventory(Script.Inventory):
	        import pyre.inventory as inv 
	        mdEngine = inv.facility('mdEngine', default='gulp')
	        mdEngine.meta['known_plugins'] = ['gulp','mmtk']
	        mdEngine.meta['tip'] = 'which md engine to use'
	
	    def __init__(self):
	        Script.__init__(self, 'MdApp')
	        self.i = self.inventory
	        
	    def main(self, *args, **kwds):
	        self.i.mdEngine.execute()
	
	if __name__=='__main__':
	    app=MdApp()
	    app.run()
