# -*- coding: UTF-8 -*-

"""https://stackoverflow.com/a/46144596/13026442
"""

###############################################################################

import asyncio

from kiwifarmer.utils import (
  download_many_files, )

###############################################################################

URL_LIST_FILE = '../../data_20210224/connection_url_list.txt'

OUTPUT_DIR = '../../data_20210224/downloaded_members_connections'

SEMAPHORE = 20

THRESHOLD_KB = 15

###############################################################################

URL_BASE = 'https://kiwifarms.net/members/'

def filename_to_url( filename ):
  return URL_BASE + '/'.join( filename.split( '.' )[ 0 ].split( '_' ) )

def url_to_filename( url ):
  return '_'.join( url.split( '/' )[ -3 :  ] ) + '.html'

###############################################################################

with open( URL_LIST_FILE, 'r' ) as f:
  url_list = f.read().split('\n')

url_list = list( filter( None, url_list ) )

asyncio.run( download_many_files(
  url_list = url_list,
  output_dir = OUTPUT_DIR,
  semaphore = SEMAPHORE,
  threshold_kb = THRESHOLD_KB,
  filename_to_url = filename_to_url,
  url_to_filename = url_to_filename ) )

###############################################################################