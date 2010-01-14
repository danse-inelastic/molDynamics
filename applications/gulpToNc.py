#!/usr/bin/env python

import sys,os

dir='graphKH-70K-test'
new=dir+'.nc'

os.system('python dlpoly_to_nc '+dir+' '+new)
