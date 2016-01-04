#!/usr/bin/env python
import unittest
import os
from coverage import coverage
from tests import *

if __name__ == '__main__':
    cov = coverage(branch=True, include=['appstore/*'])
    cov.start()

    try:
        suite = unittest.TestLoader().discover('tests/', pattern="test_*.py")
        unittest.TextTestRunner(verbosity=2).run(suite)
    except:
        pass

    cov.stop()
    cov.save()
    print("\n\nCoverage Report:\n")
    cov.report()
    print("HTML version: " + os.path.join('tmp','coverage','index.html'))
    cov.html_report(directory=os.path.join('tmp','coverage'))
    cov.erase()
