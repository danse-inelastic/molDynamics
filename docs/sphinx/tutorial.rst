.. _tutorial:

Tutorial
=========

Running memd
--------------

As memd is a pyre application, it engines are facilities that can be set at runtime.  The internal code for memd as a pyre application is called Memd.py.  One may see its simple structure and two engines in its inventory:

.. literalinclude:: ../../applications/Memd.py
   :lines: 11-33

Running the code is simple::

	memd.py --engine=gulp --engine.runType=md ...

where each option is given as key value pairs.  Settings may also be input using an xml file, called a pml file in pyre lingo, or using a UI framework that can introspect pyre components and create widgets automatically, such as `luban <http://docs.danse.us/pyre/luban/sphinx/index.html>`_. Examples of pml files for major workflows are given below.

Configuring memd for atomic structure optimization
---------------------------------------------------

To optimize the coordinates of an atomic structure one may try the following set of configurations:

.. literalinclude:: ../../useCases/gulp/kc24Optimize/Memd.pml

Configuring memd for lattice dynamics
------------------------------------------

To configure memd for a lattice dynamics calculation for potassium intercalated graphite, use the following set of configurations:

.. literalinclude:: ../../useCases/gulp/kc24Phonons/Memd.pml

Configuring memd for md using the Gulp engine
-----------------------------------------------

To configure a memd run for potassium intercalated graphite, for example, one may use the following set of configurations:

.. literalinclude:: ../../useCases/gulp/kc24Md/Memd.pml

Configuring memd for md using the Mmtk engine
-----------------------------------------------

In general MMTK is limited to molecules and ions described by the Amber 94 forcefield.  However, it can also do simple lennard jones materials.  This example shows a simulation of Argon using such a potential:

.. literalinclude:: ../../useCases/mmtk/Memd.pml



