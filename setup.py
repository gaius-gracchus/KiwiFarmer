# -*- coding: UTF-8 -*-

import os.path
from setuptools import setup

def readme( ):

  with open( os.path.abspath(
    os.path.join(
      os.path.dirname( __file__ ),
      'README.rst' ) ) ) as f:

    return f.read( )

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
    'requests >= 2.20',
    'beautifulsoup4 >= 4.8.1',
    'mysql-connector-python >= 8.0.19' ],
  extras_require = {
    'docs': [
      'sphinx >= 2.1',
      'sphinx_rtd_theme >= 0.4',
      'aiohttp >= 3.6.2',
      'aiofiles >= 0.4.0' ] },
  include_package_data = True,
  zip_safe = False )