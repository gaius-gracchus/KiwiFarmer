# -*- coding: UTF-8 -*-

"""Generate list of all `page_url`s for all threads, using as input the directory
containing the HTML files for all threads.

"""

###############################################################################

import os
import asyncio

from bs4 import BeautifulSoup
import aiofiles
from aiohttp import ClientSession

from kiwifarmer import functions

###############################################################################

INPUT_DIR = 'downloaded'

OUTPUT_DIR = 'downloaded_pages'

###############################################################################

files = sorted( os.listdir( INPUT_DIR ) )
thread_output_dir = [ file[:-5] for file in files ]

all_pages = [ ]

for file in files:

  thread_output_dir = file[:-5]

  with open( os.path.join( INPUT_DIR, file ), 'r' ) as f:
    soup = BeautifulSoup( f.read( ), 'lxml' )

  last_page = functions.get_thread_last_page( soup = soup )

  pages = [ 'https://kiwifarms.net/threads/' + file[:-5] + f'/page-{i}/' for i in range( 1, last_page + 1 ) ]

  all_pages.extend( pages )

with open( 'all_page_urls.txt', 'w' ) as f:
  for page in all_pages:
    f.write( page + '\n' )

###############################################################################
