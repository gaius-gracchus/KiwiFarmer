# -*- coding: UTF-8 -*-

###############################################################################

import unittest

from . import functions

def test_suite( ):

  all_suites = list( )

  all_suites += functions.test_suite( )

  return unittest.TestSuite( all_suites )

###############################################################################
