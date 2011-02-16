
from memdf.gulp.Visitor import Visitor
from os import linesep


class OptionWriter(Visitor):
    
    def __init__(self,sampleReference):
        self.sample=sampleReference
        
    def writeGeneralOptions(self,gulp):
        '''write common option for all types of runs'''
        # coordinate writing is difficult in gulp so use object
        #coords=Coordinates(self.i)
        #commonOptions = self.writeUnitCell()
        #commonOptions+= coords.write()
        # however, for now we'll bypass the above and write the input file directly onto gulp input file
        commonOptions = gulp.sample.atomicStructure.gulpFormatUcNAtoms(gulp.runType)
        commonOptions += gulp.potential.forcefield.writeGulp()
        return commonOptions
    
    def writeMdOptions(self,mdRuntype):
        '''write molecular dynamics information'''
        lines=self.writeEnsemble(mdRuntype)+\
        self.writeExternalConditions(mdRuntype)+\
        'equilibration '+str(mdRuntype.equilibrationTime)+' ps'+linesep+\
        'production '+str(mdRuntype.productionTime)+' ps'+linesep+\
        'timestep '+str(mdRuntype.timeStep)+' fs'+linesep+\
        'sample '+str(mdRuntype.sampleFrequency)+' fs'+linesep+\
        self.outputOptions(mdRuntype)
        return lines
        
    def outputOptions(self,mdRuntype):
        '''writes output options'''
        if mdRuntype.trajectoryType=='xyz':
            lines='output movie xyz '+mdRuntype.trajectoryFilename+'.xyz'+linesep
        elif mdRuntype.trajectoryType=='history':
            lines='output history '+mdRuntype.trajectoryFilename+'.his'+linesep
        elif mdRuntype.trajectoryType=='xyz and history':
            lines='output movie xyz '+mdRuntype.trajectoryFilename+'.xyz'+linesep+\
                    'output history '+mdRuntype.trajectoryFilename+'.his'+linesep
        lines+='write '+str(mdRuntype.dumpFrequency)+' ps'+linesep#+\
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
                
    def writeExternalConditions(self,mdRuntype):
        '''writes external tp conditions'''
        conditions=''
        if mdRuntype.ensemble=='nve':
            conditions+='temperature '+str(self.sample.temperature)+linesep
        elif mdRuntype.ensemble=='nvt': 
            conditions+='temperature '+str(self.sample.temperature)+linesep
        elif mdRuntype.ensemble=='npt': 
            conditions+='temperature '+str(self.sample.temperature)+linesep
            conditions+='pressure '+str(self.sample.pressure)+linesep
        return conditions
    
    def writePotentialOptions(self, potential):
        pass
    
    def writePhononOptions(self,phononRuntype):
        '''write phonon information'''
        lines='shrink '+phononRuntype.kpointMesh+linesep+\
        self.writeProjectDos(phononRuntype)+\
        'output phonon '+phononRuntype.dosAndDispersionFilename+linesep+\
        'output frequency '+phononRuntype.dosAndDispersionFilename+linesep
        return lines
    
    def writeProjectDos(self, phononRuntype):
        '''write the phonon projection'''
        projectedSpecies=phononRuntype.projectDos.split()
        lines='project '+str(len(projectedSpecies))+linesep
        for atom in projectedSpecies:
            lines=lines+atom+linesep
        return lines
    
    def writeOptimizeOptions(self,runtype):
        '''write optimization information'''
        lines=''
        lines+='output movie xyz '+runtype.trajectoryFilename+'.xyz'+linesep
        lines+='dump '+runtype.restartFilename+linesep
        return lines
    
    def writeFitOptions(self,runtype):
        '''write fitting information'''
        pass
        
    
        