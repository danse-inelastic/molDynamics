#!/usr/bin/env sh

svn up
scp -r _build/html/ jbrkeith@login.cacr.caltech.edu:molDynamics
