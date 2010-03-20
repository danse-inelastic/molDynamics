
from molDynamics.gulp.Visitor import Visitor
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
        commonOptions = gulp.i.sample.i.atomicStructure.gulpFormatUcNAtoms(gulp.i.runType)
        commonOptions += gulp.i.potential.i.forcefield.writeGulp()
        return commonOptions
    
    def writeMdOptions(self,mdRuntype):
        '''write molecular dynamics information'''
        lines=self.writeEnsemble(mdRuntype)+\
        self.writeExternalConditions(mdRuntype)+\
        'equilibration '+str(mdRuntype.i.equilibrationTime)+' ps'+linesep+\
        'production '+str(mdRuntype.i.productionTime)+' ps'+linesep+\
        'timestep '+str(mdRuntype.i.timeStep)+' fs'+linesep+\
        'sample '+str(mdRuntype.i.sampleFrequency)+' fs'+linesep+\
        self.outputOptions(mdRuntype)
        return lines
        
    def outputOptions(self,mdRuntype):
        '''writes output options'''
        if mdRuntype.i.trajectoryType=='xyz':
            lines='output movie xyz '+mdRuntype.i.trajectoryFilename+'.xyz'+linesep
        elif mdRuntype.i.trajectoryType=='history':
            lines='output history '+mdRuntype.i.trajectoryFilename+'.his'+linesep
        elif mdRuntype.i.trajectoryType=='xyz and history':
            lines='output movie xyz '+mdRuntype.i.trajectoryFilename+'.xyz'+linesep+\
                    'output history '+mdRuntype.i.trajectoryFilename+'.his'+linesep
        lines+='write '+str(mdRuntype.i.dumpFrequency)+' ps'+linesep#+\
        lines+='dump '+mdRuntype.i.restartFilename+linesep
        # don't write the following line for now--it's probably for optimization only
        #'dump every '+str(self.i.dumpFrequency)+linesep
        return lines
    
    def writeEnsemble(self,mdRuntype):
        '''write the thermodynamic ensemble'''
        if mdRuntype.i.ensemble=='nve':
            return 'ensemble '+mdRuntype.i.ensemble+linesep
        elif mdRuntype.i.ensemble=='nvt':
            return 'ensemble '+mdRuntype.i.ensemble+' '+str(mdRuntype.i.thermostatParameter)+linesep
        elif mdRuntype.i.ensemble=='npt':
            return 'ensemble '+mdRuntype.i.ensemble+' '+str(mdRuntype.i.thermostatParameter)\
                +' '+str(mdRuntype.i.barostatParameter)+linesep
                
    def writeExternalConditions(self,mdRuntype):
        '''writes external tp conditions'''
        conditions=''
        if mdRuntype.i.ensemble=='nve':
            conditions+='temperature '+str(self.sample.i.temperature)+linesep
        elif mdRuntype.i.ensemble=='nvt': 
            conditions+='temperature '+str(self.sample.i.temperature)+linesep
        elif mdRuntype.i.ensemble=='npt': 
            conditions+='temperature '+str(self.sample.i.temperature)+linesep
            conditions+='pressure '+str(self.sample.i.pressure)+linesep
        return conditions
    
    def writePotentialOptions(self, potential):
        pass
    
    def writePhononOptions(self,phononRuntype):
        '''write phonon information'''
        lines='shrink '+phononRuntype.i.kpointMesh+linesep+\
        self.writeProjectDos(phononRuntype)+\
        'output phonon '+phononRuntype.i.dosAndDispersionFilename+linesep+\
        'output frequency '+phononRuntype.i.dosAndDispersionFilename+linesep
        return lines
    
    def writeProjectDos(self, phononRuntype):
        '''write the phonon projection'''
        projectedSpecies=phononRuntype.i.projectDos.split()
        lines='project '+str(len(projectedSpecies))+linesep
        for atom in projectedSpecies:
            lines=lines+atom+linesep
        return lines
    
    def writeOptimizeOptions(self,runtype):
        '''write optimization information'''
        lines=''
        lines+='output movie xyz '+runtype.i.trajectoryFilename+'.xyz'+linesep
        lines+='dump '+runtype.i.restartFilename+linesep
        return lines
    
    def writeFitOptions(self,runtype):
        '''write fitting information'''
        pass
        
    
        