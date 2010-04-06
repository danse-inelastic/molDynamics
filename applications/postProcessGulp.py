#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Brandon Keith
#                      California Institute of Technology
#              (C) 2005 All Rights Reserved  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from pyre.applications.Script import Script
from vsat.trajectory.ConvertFromGulpDLPOLY import ConvertFromGulpDLPOLY
import os

class PostProcessGulp(Script):
    '''Various conversion and postprocessing routines for animation, 
    generating scattering kernels'''
    class Inventory(Script.Inventory):
        import pyre.inventory as inv 
        #task
        convertHistoryFile = inv.bool('convertHistoryFile', default=False)
        #params
        historyFile = inv.str('historyFile', default='.')
        historyFile.meta['tip'] = 'history file to translate'
        ncFile = inv.str('ncFile', default='ncFile')
        ncFile.meta['tip'] = 'new nc file to write'
        #task
        serializePhononArrays = inv.bool('serializePhononArrays', default=False)
        #params
        gulpOutputFile = inv.str('gulpOutputFile', default='gulp.gout')
        #task
        createPhononAnimation = inv.bool('createPhononAnimation', default=False)
        #params
        gulpOutputFile = inv.str('gulpOutputFile', default='gulp.gout')
        vibrationsFile = inv.str('vibrationsFile', default='vibrations.xyz')
        #task
        thinTrajectory = inv.bool('thinTrajectory', default=False)
        #
        oldTrajectory = inv.str('oldTrajectory', default='gulp.nc')
        newTrajectory = inv.str('newTrajectory', default='gulp2.nc')

    def __init__(self):
        Script.__init__(self, 'PostProcessGulp')
        
    def _configure(self):
        self.historyFile = self.inventory.historyFile
        self.ncFile = self.inventory.ncFile
        self.gulpOutputFile = self.inventory.gulpOutputFile
        self.vibrationsFile = self.inventory.vibrationsFile
        
    def main(self, *args, **kwds):
        if self.inventory.convertHistoryFile:
            c = ConvertFromGulpDLPOLY()
            c.setHistoryFileName(self.historyFile)
            c.setNetcdfFile(self.ncFile)
            c.convert()
            os.remove(self.historyFile)
        if self.inventory.thinTrajectory:
            #actually, all i need to do here is just create new time dimension and then
            #create new variables for kinetic energy, etc....but first be sure to just run normal
            #gulp at 60,80K to look for signs of vacacy diffusion (where quantum correction doesn't matter so much)
#            from Scientific.IO.NetCDF import NetCDFFile
#            self.file = NetCDFFile(self.inventory.oldTrajectory, 'r')
#            self.file2 = NetCDFFile(self.inventory.newTrajectory, 'w')
#            for key,val in self.file.dimensions.iteritems():
#                self.file2.createDimension(key, val)
#                
#            for key,val in self.file.variables.iteritems():
#                self.file2.createVariable(key, val, )
#            from vsat.Trajectory import Trajectory
#            trajOriginal=Trajectory()
            
        if self.inventory.serializePhononArrays:
            from memd.gulp.output.OutputParser import OutputParser
            o = OutputParser(self.gulpOutputFile, runtype = 'phonons')
            #pickle it
            phonons = o.getEigsAndVecs()
            phonons.write()
#        if self.inventory.createPhononAnimation:
#            o = OutputParser(gulpOutputFile=self.gulpOutputFile)
#            o.outputVibrationsFile(self.vibrationFilename)
        
        

if __name__=='__main__':
    app = PostProcessGulp()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
