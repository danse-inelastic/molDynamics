#!/usr/bin/env python
from memdf.gulp.Optimize import Optimize
m = Optimize()
m.xyzFile='structure.xyz'
m.forcefield='axiallySymmetricNWS.lib'
m.inputDeckName = 'mOpt.gin'
m.writeInputfile()

from memdf.gulp.Phonon import Phonon
m = Phonon()
m.xyzFile='structure.xyz'
m.forcefield='axiallySymmetricNWS.lib'
m.inputDeckName = 'mPhon.gin'
m.writeInputfile()

from memdf.gulp.Md import Md
m = Md()
m.xyzFile='structure.xyz'
m.forcefield='axiallySymmetricNWS.lib'
m.inputDeckName = 'mMd.gin'
m.writeInputfile()


