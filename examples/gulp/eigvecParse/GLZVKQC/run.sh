#!/usr/bin/env sh
. ~/.gulp-env
chmod +x run1.sh
mpirun -np 1 ./run1.sh

postProcessGulp.py --historyFile=output.history --ncFile=output.nc