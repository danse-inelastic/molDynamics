#
from matter import Structure
kc24 = Structure().read('kc24Relaxed.xyz')
from memd2.gulp.Gulp import Gulp
gulp = Gulp(runtype = 'md')
gulp.matter = kc24
gulp.timesteps = 5
gulp.execute()
