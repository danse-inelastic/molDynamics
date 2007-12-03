#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  
# 
#  <LicenseText>
# 
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from mmtkTests.Mmtk_TestCase import *
from gulpTests.Gulp_TestCase import *

import unittest

if __name__ == "__main__":
    suite1 = unittest.makeSuite(MmtkMd_TestCase)
    suite2 = unittest.makeSuite(MmtkRestart_TestCase)
    suite3 = unittest.makeSuite(GulpMD_TestCase)
    suite4 = unittest.makeSuite(GulpOpt_TestCase)
    suite5 = unittest.makeSuite(GulpFit_TestCase)
    suite6 = unittest.makeSuite(GulpRestart_TestCase)
    alltests = unittest.TestSuite((suite1,suite3,suite4,suite5,suite6))
    alltests = unittest.TestSuite((suite1))
    unittest.TextTestRunner(verbosity=2).run(alltests)


# version
__id__ = "$Id: alltest.py 71 2005-04-07 23:07:02Z mmckerns $"

#  End of file 
