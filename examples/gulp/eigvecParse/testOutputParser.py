#!/usr/bin/env python

gulpOutputFile = "GLZVKQC/gulp.gout"

from memd.gulp.output.OutputParser import OutputParser
o = OutputParser(gulpOutputFile, runtype = 'phonons')
phonons = o.getEigsAndVecs()
print phonons.energies
#pickle it
phonons.write(['energies.pkl','polarizations.pkl'])

#phonons.energies=None
#phonons.polarizations=None
#phonons.read(('energies.pkl','polarizations.pkl'))
#print 'restored'
#print phonons.energies[0]
#print phonons.polarizations[0]

#or
print 'pickle load'

import numpy
energies = numpy.load('energies.pkl')
print energies[0]