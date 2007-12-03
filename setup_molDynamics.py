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
        sourceDir = 'molDynamics',
        destModuleName = 'molDynamics' )

    package.addScripts( sourceFiles = [
        "applications/MdApp.py"
        ] )

    package.addEtc( "etc" )
    return package


if __name__ == "__main__":
    from distutils_adpt.Package import Package
    package = Package('molDynamics', '1.0')
    preparePackage(package)
    package.setup()

