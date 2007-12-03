#!/usr/bin/env python

def preparePackage( package, sourceRoot = "." ):
    package.changeRoot( sourceRoot )
    #------------------------------------------------------------
    #dependencies
    #
    #------------------------------------------------------------

    #--------------------------------------------------------
    # now add subdirs
    #
    package.addPurePython(
        sourceDir = 'mmtk',
        destModuleName = 'mmtk' )

    return package


if __name__ == "__main__":
    from distutils_adpt.Package import Package
    package = Package('mmtk', '0.1')

    preparePackage( package )

    package.setup()

