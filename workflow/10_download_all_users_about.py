# -*- coding: UTF-8 -*-

"""https://stackoverflow.com/a/46144596/13026442
"""

###############################################################################

import asyncio

from kiwifarmer.utils import (
  page_filename_to_url,
  page_url_to_filename,
  download_many_files, )

###############################################################################

URL_LIST_FILE = '../../data_20210224/member_url_list.txt'

OUTPUT_DIR = '../../data_20210224/downloaded_members_about'

SEMAPHORE = 20

THRESHOLD_KB = 15

###############################################################################

with open( URL_LIST_FILE, 'r' ) as f:
  url_list = f.read().split('\n')

url_list = list( filter( None, url_list ) )
url_list = [ url + 'about' for url in url_list ]

filename_list = list( range( len( url_list ) ) )
filename_list = [ str( e ) + '.html' for e in filename_list ]

url_to_filename = dict( zip( url_list, filename_list ) )
filename_to_url = dict( zip( filename_list, url_list ) )

asyncio.run( download_many_files(
  url_list = url_list,
  output_dir = OUTPUT_DIR,
  semaphore = SEMAPHORE,
  threshold_kb = THRESHOLD_KB,
  filename_to_url = filename_to_url.get,
  url_to_filename = url_to_filename.get ) )

###############################################################################