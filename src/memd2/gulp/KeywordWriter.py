
from molDynamics.gulp.Visitor import Visitor


class KeywordWriter(Visitor):
    
    def writeGeneralKeywords(self, gulp):
        '''write the general keywords for gulp'''
        # these next lines insert 'molecule' in the keyword list if any potentials
        # are signaled as intramolecular
#        for ff in self.i.sample.i.forcefields:
#            if ff.i.interIntra!=None and 'molecule' not in self.keywords: 
#                self.keywords+=['molecule']
        keywords=[]
        if gulp.i.computeMaterialProperties:
            keywords+=['property']
        return keywords

    def writeMdKeywords(self, md):
        '''writes the md keywords'''
        keywords=[]
        if md.i.ensemble=='nve' or md.i.ensemble=='nvt':
            keywords=['md','conv']+keywords
        elif md.i.ensemble=='npt': 
            keywords=['md','conp']+keywords
        return keywords
    
    def writePhononKeywords(self, phonon):
        '''writes the phonon keywords'''
        keywords=[]
        # add phonon keyword first
        keywords+=['phonon']
        # broaden the dos
        if phonon.i.broadenDos:
            keywords+=['broaden_dos']
        return keywords
    
    def writeFitKeywords(self, runtype):
        '''writes the fit keywords'''
        keywords=[]
        if runtype.i.constraints=='None':
            keywords+= ['noflags']
        if runtype.i.constraints=='constant volume':
            keywords+= ['conv']
        elif runtype.i.constraints=='constant pressure':
            keywords+= ['conp']      
        keywords+=['fit']
        return keywords
    
    def writePotentialKeywords(self, potential):
        keywords=[]
        if potential.i.moleculeIdentification=='identify molecules; remove intramolecular Coulomb forces':
            keywords+=['molecule']
        elif potential.i.moleculeIdentification=='identify molecules; retain intramolecular Coulomb forces':
            keywords+=['molq']
        if potential.i.dispersionInRecipSpace==True:
            keywords+=['c6']
        if potential.i.useInitialBondingOnly==True:
            keywords+=['fix']
        return keywords
    
    def writeOptimizeKeywords(self,runtype):
        '''write optimization information'''
        keywords=[]
        if runtype.i.constraints=='constant volume':
            keywords+= ['conv']
        elif runtype.i.constraints=='constant pressure':
            keywords+= ['conp']      
        keywords+=['optimise']
        return keywords
    



    