from memd.gulp.Visitor import Visitor

class KeywordWriter(Visitor):
    
    def writeGeneralKeywords(self, gulp):
        '''write the general keywords for gulp'''
        # these next lines insert 'molecule' in the keyword list if any potentials
        # are signaled as intramolecular
#        for ff in self.sample.forcefields:
#            if ff.interIntra!=None and 'molecule' not in self.keywords: 
#                self.keywords+=['molecule']
        keywords=[]
        if gulp.computeMaterialProperties:
            keywords+=['property']
        return keywords

    def writeMdKeywords(self, md):
        '''writes the md keywords'''
        keywords=[]
        if md.ensemble=='nve' or md.ensemble=='nvt':
            keywords=['md','conv']+keywords
        elif md.ensemble=='npt': 
            keywords=['md','conp']+keywords
        return keywords
    
    def writePhononKeywords(self, phonon):
        '''writes the phonon keywords'''
        keywords=[]
        # add phonon keyword first
        keywords+=['phonon']
        # broaden the dos
        if phonon.broadenDos:
            keywords+=['broaden_dos']
        return keywords
    
    def writeFitKeywords(self, runtype):
        '''writes the fit keywords'''
        keywords=[]
        if runtype.constraints=='None':
            keywords+= ['noflags']
        if runtype.constraints=='constant volume':
            keywords+= ['conv']
        elif runtype.constraints=='constant pressure':
            keywords+= ['conp']      
        keywords+=['fit']
        return keywords
    
    def writePotentialKeywords(self, potential):
        keywords=[]
        if potential.moleculeIdentification=='identify molecules; remove intramolecular Coulomb forces':
            keywords+=['molecule']
        elif potential.moleculeIdentification=='identify molecules; retain intramolecular Coulomb forces':
            keywords+=['molq']
        if potential.dispersionInRecipSpace==True:
            keywords+=['c6']
        if potential.useInitialBondingOnly==True:
            keywords+=['fix']
        return keywords
    
    def writeOptimizeKeywords(self,runtype):
        '''write optimization information'''
        keywords=[]
        if runtype.constraints=='constant volume':
            keywords+= ['conv']
        elif runtype.constraints=='constant pressure':
            keywords+= ['conp']      
        keywords+=['optimise']
        return keywords
    
    def writeGulpKeywords(self, gulp):
        keywords=[]
        keywords+=self.writeGeneralKeywords(gulp)
        keywords+=self.writePotentialKeywords(gulp)
        return keywords


    