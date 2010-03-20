
Configuring memd for lattice dynamics
======================================

To configure memd for a lattice dynamics calculation of fcc Al, one performs the following steps

.. literalinclude:: ../../useCases/gulp/kc24Md/memdLd.py

Configuring memd for md using Gulp engine
=========================================

To configure a memd run for potassium intercalated graphite, one performs the following steps::

.. literalinclude:: ../../useCases/gulp/kc24Md/memdMd.py

Configuring memd for md using Mmtk engine
=========================================

In general MMTK is limited to molecules and ions described by the Amber 94 forcefield, so we choose a molecular crystal, benzene, at slightly elevated pressure (0.30 GPa).  After storing this in the database

To configure a memd run for potassium intercalated graphite, one performs the following steps::

.. literalinclude:: ../../useCases/gulp/kc24Md/memdMd.py

.. index:: swap-md-engines

Running memd
============

As memd is a pyre application, it engines are facilities that can be set at runtime.  The internal code for memd as a pyre application is called MdApp.py.  One may see its simple structure and two engines in its inventory:

.. literalinclude:: ../../applications/MdApp.py
   :lines: 11-33




Running the code is very simple:

Storing settings
=================


(optional) Creating dataobjects from results
=============================================

Memd produces a variety of dynamical information about a system.  It uses the Vsat data objects to encapsulate this information so it can be stored in a db or serialized for later retrieval.  Creating these data objects is simple:

Getting Vibrations from MEMD:
--------------------------------



.. _getMotion:

Getting Motion from MEMD:
-------------------------

To get a Motion data object from an MEMD output file:

Gulp engine:
^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: examples/CreateMotionDo.py


Mmtk engine:
^^^^^^^^^^^^^^^^^^^^

