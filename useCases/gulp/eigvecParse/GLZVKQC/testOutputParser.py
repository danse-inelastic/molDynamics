#!/usr/bin/env python

gulpOutputFile = "gulp.gout"

from memd.gulp.output.OutputParser import OutputParser
o = OutputParser(gulpOutputFile, runtype = 'phonons')
phonons = o.getEigsAndVecs()
print phonons.energies[0,0,0]
#pickle it
phonons.write(['energies.pkl','polarizations.pkl'])

phonons.energies=None
phonons.polarizations=None
phonons.read()
print 'restored'
print phonons.energies[0,0,0]
print phonons.polarizations[0]

#or
print 'pickle load'

import numpy
energies = numpy.load('energies.pkl')
print energies[0]