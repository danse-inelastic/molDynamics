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
        extractPhonons = inv.bool('extractPhonons', default=False)
        #params
        gulpOutputFile = inv.str('gulpOutputFile', default='gulp.gout')
        phononsFile = inv.str('phononsFile', default='phonons.pkl')
        #task
        createPhononAnimation = inv.bool('createPhononAnimation', default=False)
        #params
        gulpOutputFile = inv.str('gulpOutputFile', default='gulp.gout')
        vibrationsFile = inv.str('vibrationsFile', default='vibrations.xyz')

    def __init__(self):
        Script.__init__(self, 'PostProcessGulp')
        
    def _configure(self):
        self.historyFile = self.inventory.historyFile
        self.ncFile = self.inventory.ncFile
        self.gulpOutputFile = self.inventory.gulpOutputFile
        self.vibrationsFile = self.inventory.vibrationsFile
        self.phononsFile = self.inventory.phononsFile
        
    def main(self, *args, **kwds):
        if self.inventory.convertHistoryFile:
            c = ConvertFromGulpDLPOLY()
            c.setHistoryFileName(self.historyFile)
            c.setNetcdfFile(self.ncFile)
            c.convert()
        if self.inventory.extractPhonons:
            from memd.gulp.output.OutputParser import OutputParser
            o = OutputParser(self.gulpOutputFile, runtype = 'phonons')
            #pickle it
            o.pickleEigsAndVecs(self.phononsFile)
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
