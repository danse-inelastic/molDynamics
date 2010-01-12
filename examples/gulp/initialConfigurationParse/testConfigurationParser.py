#!/usr/bin/env python

gulpFile = "gulp.out"

from kernelGenerator.gulp.OutputParser import OutputParser
o = OutputParser(gulpFile,'phonons')
phonons = o.getEigsAndVecs()

print phonons.frequencies
print phonons.modes