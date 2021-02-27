# -*- coding: UTF-8 -*-

"""https://stackoverflow.com/a/46144596/13026442
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import asyncio

from kiwifarmer.utils import (
  page_filename_to_url,
  page_url_to_filename,
  download_many_files, )
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

URL_LIST_FILE = '../../data_20210224/page_url_list.txt'

OUTPUT_DIR = '../../data_20210224/downloaded_pages'

SEMAPHORE = 20

THRESHOLD_KB = 20

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

with open( URL_LIST_FILE, 'r' ) as f:
  url_list = f.read().split('\n')

asyncio.run( download_many_files(
  url_list = url_list,
  output_dir = OUTPUT_DIR,
  semaphore = SEMAPHORE,
  threshold_kb = THRESHOLD_KB,
  filename_to_url = page_filename_to_url,
  url_to_filename = page_url_to_filename ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#