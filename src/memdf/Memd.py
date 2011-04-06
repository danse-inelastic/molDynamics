
class Memd(object):
    '''Driver for the md engines in DANSE.'''
    engine = 'gulp'
    #
    xyzFile=''
    temperature=0.0
    pressure=0.0
    #
    dispersionInRecipSpace = False
    useInitialBondingOnly = False
    forcefield = ''
    moleculeIdentification = 'None'
    #
    constraints = 'None'
    #['None', 'constant_volume', 'constant_pressure'
    optimizeCell = False
    optimizeCoordinates = False
    trajectoryFilename = 'molDynamics'
    restartFilename = 'molDynamics.res'
    #
    kpointMesh = ''
    dosAndDispersionFilename = ""
    broadenDos = False
    projectDos = ''
    #
    ensemble = 'nvt'
    equilibrationTime = 0.0
    productionTime = 0.0
    propCalcInterval = 5.0
    thermostatParameter = 0.05
    barostatParameter = 0.0
    timeStep = 0.002
    trajectoryFilename = 'molDynamics.his'
    restartFilename = 'molDynamics.res'
    dumpInterval = 0.0    

    def __init__(self, **kwds):
        for k, v in kwds.iteritems():
            setattr(self, k, v)  
        
    def writeInputFile(self):
        settings={}
        d = dir(self)
        #publicFunctions = ['writeInputFile','Inventory','customizeLubanObjectDrawer']
        for key in d:
            if key[0]=='_':# or key in publicFunctions:
                pass
            else:
                settings[key] = getattr(self, key)
        if self.engine=='gulp':
            from gulp.Gulp import Gulp
            e=Gulp(kwds=settings)
            e.writeInputfile()
        elif self.engine=='mmmtk':
            from mmtk.Mmtk import Mmtk
            e=Mmtk()
        

if __name__=='__main__':
    app=Memd()
    app.run()

# version
__id__ = "$Id$"

# Generated automatically by PythonMill on Tue Jun  5 15:04:48 2007

# End of file 
