#!/usr/bin/env python

gulpFile = "GLZVKQC/gulp.gout"

from memd.gulp.output.OutputParser import OutputParser
o = OutputParser(gulpFile,'phonons')
phonons = o.getEigsAndVecs()
print phonons.frequencies
print phonons.modes
kpts = o.getKpoints()
print kpts