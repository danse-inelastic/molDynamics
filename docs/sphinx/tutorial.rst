


.. index:: swap-md-engines

Science Tutorial: Switching computational engines
=================================================

Let us demonstrate how to switch computational engines.  First, we us MdApp.py, a simple pyre application with two engines in its inventory:

.. literalinclude:: ../../applications/MdApp.py
   :lines: 11-33

In general MMTK is limited to molecules and ions described by the Amber 94 forcefield, so we choose a molecular crystal, benzene, at slightly elevated pressure (0.30 GPa).  After storing this in the database


Running the code is very simple:

