#!/usr/bin/env python
from memdf.Memd import Memd

m = Memd()
m.engineType = 'gulp'
m.temperature = 300

m.writeInputfile()

