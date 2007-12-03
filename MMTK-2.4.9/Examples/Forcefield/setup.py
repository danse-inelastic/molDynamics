# Use this script to compile the C module by running
#
#         python setup.py build
#
# and copying the compiled module from the directory 'build'.

from distutils.core import setup, Extension

setup (name = "HarmonicOscillatorForceField",
       version = "1.0",
       description = "Harmonic Oscillator forcefield term for MMTK",

       py_modules = ['HarmonicOscillatorFF'],
       ext_modules = [Extension('MMTK_harmonic_oscillator',
                                ['MMTK_harmonic_oscillator.c'])]
       )
