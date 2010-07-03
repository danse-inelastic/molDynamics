#
from matter import Structure
kc24 = Structure().read('kc24Relaxed.xyz')
from memd2.gulp.Gulp import Gulp
gulp = Gulp()
gulp.matter = kc24
gulp.runtype = 'md'
gulp.productionTime = 0.005
gulp.execute()
