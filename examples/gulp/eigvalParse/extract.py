

if __name__=='__main__':
    from memd.gulp.output.OutputParser import OutputParser
    op = OutputParser('FMKTSGU/gulp.gout', runtype='phonons')
    phonons = op.getEigvals()
    print phonons.frequencies