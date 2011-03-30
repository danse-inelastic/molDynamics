
from memd.gulp.Visitor import Visitor
from os import linesep


class OptionWriter(Visitor):
    
    def __init__(self):
        self.atomStrings = None
        self.ucVecs = None
        
    def initializeFromFile(self,gulp):
        try:
            f=file(gulp.xyzFile)
        except:
            print "cannot open xyz file"
            raise
        self.atomStrings = f.readlines()
        try:
            ax,ay,az,bx,by,bz,cx,cy,cz = self.atomStrings[1].split()
            self.ucVecs = [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]
        except:
            ax,ay,az,bx,by,bz,cx,cy,cz = 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0
            self.ucVecs = [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]
        return ax,ay,az,bx,by,bz,cx,cy,cz

    def gulpFormatUcNAtoms(self,gulp):
#        try:
#            f=file(self.i.inputFile)
#        except:
#            print "cannot open xyz file"
#            raise
#        lines=f.readlines()
#        ax,ay,az,bx,by,bz,cx,cy,cz = self.ucVecs
        ax,ay,az,bx,by,bz,cx,cy,cz = self.initializeFromFile(gulp)
        text='vectors'+linesep + ax+' '+ay+' '+az + linesep + bx+' '+by+' '+bz+linesep + cx+' '+cy+' '+cz+linesep
        if gulp.__class__.__name__=='Optimize':
            if gulp.optimizeCell:
                #remove the last linesep and add the optimize flags
                text=text[:-1]+' 1 1 1 1 1 1'+linesep
        text+='cartesian'+linesep
        for line in self.atomStrings[2:]:
            text+=line
        text+=linesep
        return text
    
    def getAtomsAsStrings(self):
        if not self.atomStrings:
            self.initializeFromFile()
        return self.atomStrings[2:]
    
    def getCellVectors(self):
        if not self.ucVecs:
            self.initializeFromFile()
        return self.ucVecs
    
    def writeForcefield(self,gulp):
        '''read in the file's contents and return them'''
        try:
            f=file(gulp.forcefield)
        except:
            print "cannot read forcefield file"
            raise 
        return f.read()+linesep
        
    def writeGeneralOptions(self,gulp):
        '''write common option for all types of runs'''
        # coordinate writing is difficult in gulp so use object
        #coords=Coordinates(self.i)
        #commonOptions = self.writeUnitCell()
        #commonOptions+= coords.write()
        # however, for now we'll bypass the above and write the input file directly onto gulp input file
        commonOptions = 'supercell '+gulp.supercell
        commonOptions += self.gulpFormatUcNAtoms(gulp)
        commonOptions += self.writeForcefield(gulp)
        return commonOptions
    
    def writeMdOptions(self,mdRuntype):
        '''write molecular dynamics information'''
        lines=self.writeEnsemble(mdRuntype)+\
        self.writeExternalConditions(mdRuntype)+\
        'equilibration '+str(mdRuntype.equilibrationTime)+' ps'+linesep+\
        'production '+str(mdRuntype.productionTime)+' ps'+linesep+\
        'timestep '+str(mdRuntype.timeStep)+' ps'+linesep+\
        'sample '+str(mdRuntype.propCalcInterval)+' ps'+linesep+\
        self.outputOptions(mdRuntype)
        return lines
        
    def outputOptions(self,mdRuntype):
        '''writes output options'''
        if mdRuntype.trajectoryFilename.split('.')[-1] in ['his','xyz']:
            trajectoryType=mdRuntype.trajectoryFilename.split('.')[-1]
        else:
            trajectoryType='his'
        if trajectoryType=='xyz':
            lines='output movie xyz '+self.addExtensionIfNecessary(mdRuntype.trajectoryFilename, 'xyz')+linesep
        elif trajectoryType=='his':
            lines='output history '+self.addExtensionIfNecessary(mdRuntype.trajectoryFilename, 'his')+linesep
#        elif trajectoryType=='xyz and history':
#            lines='output movie xyz '+mdRuntype.trajectoryFilename+'.xyz'+linesep+\
#                    'output history '+mdRuntype.trajectoryFilename+'.his'+linesep
        lines+='write '+str(mdRuntype.dumpInterval)+' ps'+linesep#+\
        lines+='dump '+mdRuntype.restartFilename+linesep
        # don't write the following line for now--it's probably for optimization only
        #'dump every '+str(self.dumpFrequency)+linesep
        return lines
    
    def writeEnsemble(self,mdRuntype):
        '''write the thermodynamic ensemble'''
        if mdRuntype.ensemble=='nve':
            return 'ensemble '+mdRuntype.ensemble+linesep
        elif mdRuntype.ensemble=='nvt':
            return 'ensemble '+mdRuntype.ensemble+' '+str(mdRuntype.thermostatParameter)+linesep
        elif mdRuntype.ensemble=='npt':
            return 'ensemble '+mdRuntype.ensemble+' '+str(mdRuntype.thermostatParameter)\
                +' '+str(mdRuntype.barostatParameter)+linesep
                
#    def writeExternalConditions(self,mdRuntype):
#        '''writes external tp conditions'''
#        conditions=''
#        if mdRuntype.ensemble=='nve':
#            conditions+='temperature '+str(self.sample.temperature)+linesep
#        elif mdRuntype.ensemble=='nvt': 
#            conditions+='temperature '+str(self.sample.temperature)+linesep
#        elif mdRuntype.ensemble=='npt': 
#            conditions+='temperature '+str(self.sample.temperature)+linesep
#            conditions+='pressure '+str(self.sample.pressure)+linesep
#        return conditions
                
    def writeExternalConditions(self,mdRuntype):
        '''writes external tp conditions'''
        conditions=''
        if mdRuntype.ensemble=='nve':
            conditions+='temperature '+str(mdRuntype.temperature)+linesep
        elif mdRuntype.ensemble=='nvt': 
            conditions+='temperature '+str(mdRuntype.temperature)+linesep
        elif mdRuntype.ensemble=='npt': 
            conditions+='temperature '+str(mdRuntype.temperature)+linesep
            conditions+='pressure '+str(mdRuntype.pressure)+linesep
        return conditions
    
    def writePotentialOptions(self, potential):
        return ''
    
    def writePhononOptions(self,phononRuntype):
        '''write phonon information'''
        lines='shrink '+phononRuntype.kpointMesh+linesep+\
        self.writeProjectDos(phononRuntype)+\
        'output phonon '+phononRuntype.dosAndDispersionFilename+linesep+\
        'output frequency '+phononRuntype.dosAndDispersionFilename+linesep
        #"broaden_dos " + phononRuntype.broadenDos+linesep+\
        return lines
    
    def writeProjectDos(self, phononRuntype):
        '''write the phonon projection'''
        projectedSpecies=phononRuntype.projectDos.split()
        lines='project '+str(len(projectedSpecies))+linesep
        for atom in projectedSpecies:
            lines=lines+atom+linesep
        return lines
    
    def addExtensionIfNecessary(self,filename,extension):
        if filename.split('.')>1:
            if filename.split('.')[-1]==extension:
                newname = filename
            else:
                newname = filename+'.'+extension
        else:
            newname = filename+'.'+extension
        return newname
    
    def writeOptimizeOptions(self,runtype):
        '''write optimization information'''
        trajfile = self.addExtensionIfNecessary(runtype.trajectoryFilename,'xyz')
        lines=''
        lines+='output movie xyz '+trajfile+linesep
        lines+='dump '+runtype.restartFilename+linesep
        return lines
    
    def writeFitOptions(self,runtype):
        '''write fitting information'''
        pass
        
    def writeGulpOptions(self, gulp):
        options=''
        options+=self.writeGeneralOptions(gulp)
        options+=self.writePotentialOptions(gulp)
        return options
        