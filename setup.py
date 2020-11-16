# -*- coding: UTF-8 -*-

###############################################################################

import os.path
from setuptools import setup

###############################################################################

def readme( ):

  with open( os.path.abspath(
    os.path.join(
      os.path.dirname( __file__ ),
      'README.rst' ) ) ) as f:

    return f.read( )

###############################################################################

setup(
  name = 'kiwifarmer',
  version = '0.1',
  description = 'Scraping and storing KiwiFarms threads',
  long_description = readme( ),
  author = 'Gaius Gracchus',
  packages = [
    'kiwifarmer' ],
  test_suite = 'tests.test_suite',
  dependency_links = [ ],
  install_requires = [
    'requests >= 2.25.0',
    'beautifulsoup4 >= 4.9.3',
    'mysql-connector-python >= 8.0.22',
    'aiohttp >= 3.7.2',
    'aiofiles >= 0.6.0' ],
  extras_require = {
    'docs': [
      'sphinx >= 3.3.1',
      'sphinx_rtd_theme >= 0.5', ],
    'tests': [
      'pytest >= 6.1.2',
      'pytest-cov >= 2.10.1',
      'pytest-html >= 3.0.0',
      'pytest-metadata >= 1.10.0',
      'pytest-asyncio >= 0.14.0' ], },
  include_package_data = True,
  zip_safe = False )

###############################################################################