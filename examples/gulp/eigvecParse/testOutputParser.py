#!/usr/bin/env python

gulpFile = "GLZVKQC/gulp.gout"

from memd.gulp.output.OutputParser import OutputParser
o = OutputParser(gulpFile,'phonons')
vibs = o.getEigsAndVecs()
print vibs.eigVals
print vibs.eigVecs
kpts = o.getKpoints()
print kpts