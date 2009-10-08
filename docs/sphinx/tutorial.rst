


.. index:: swap-md-engines

Science Tutorial: Switching computational engines
=================================================

Let us demonstrate how to switch computational engines.  First, we us MdApp.py, a simple pyre application with two engines in its inventory:

.. literalinclude:: ../../applications/MdApp.py
   :lines: 11-33

..	class MdApp(Script):
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
	    
.. Now let's try this with doctest:

 .. doctest::
 >>>f = file('MdApp.py')
 >>>lines = f.read()
 >>>print lines

In general MMTK is limited to molecules and ions described by the Amber 94 forcefield, so we choose a molecular crystal, benzene, at slightly elevated pressure (0.30 GPa).  After storing this in the database


Running the code is very simple::

