import pylab as p
from kernelGenerator.gulp.DosPlottingUtils import getGulpDosRebinned

#doses = ['kc241x1x4/phon6x3PostCool.dens',
#         'kc241x1x4/phon6x3PostCoolBox8000.dens',
#         'kc24kpts1x1x6/phon6x3FineMeshVecs.dens',
#         'kc24kpts3x3x18/phon6x3FineMeshVecs3x3x18.dens',
#         'kc24sup6x3kpt1x1x1/phon6x3FineMeshVecs1x1x1.dens',
#         'kc24sup6x3kptGamma/phon6x3FineMeshVecsGamma.dens']
doses = ['dos.dens']
#plotNums = [321,322,323,324,325,326]
plotNums = [111,]

# rebin
#data=[]
for dos,plotNum in zip(doses,plotNums):
    #plot on matplotlib
    p.subplot(plotNum)
    x,y = getGulpDosRebinned(dos, 70, cutoffOfDosData = 500)
    p.plot(x,y)
    p.title(dos)

#axis([0, 60, 0, 0.001])
#legend(('expanded graphite only','first spot on the graphite/c60 sample','second spot on the graphite/c60 sample'))
#xlabel('wave number (cm^-1)')
#ylabel('signal (arbitrary units)')
#title('raman spectrum from other spectrometer')
p.show()

