#!/usr/bin/env bash
source /home/jbrkeith/.bash_profile
mpirun -np 1 gulp_openmpi < gulp.gin > gulp.gout

postProcessGulp.py -serializePhononArrays=True
postProcessGulp.py -historyFile=output.history -ncFile=output.nc