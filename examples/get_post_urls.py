# -*- coding: UTF-8 -*-

"""Test initialization of the `Thread` class.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from kiwifarmer import base, templates

###############################################################################

PAGE_DIR = '../../data_fresh/downloaded_threads'

START = 0

OUTPUT_FILE = '../../data_fresh/thread_post_url_list'

###############################################################################

if __name__ == '__main__':

  post_urls = [ ]

  pages = os.listdir( PAGE_DIR )

  for i, page_file in enumerate( pages[ START: ] ):

    print( f'{i} / {len( pages )}' )

    with open( os.path.join( PAGE_DIR, page_file ), 'r' ) as f:

      page_soup = BeautifulSoup( f.read( ), 'lxml' )

    page = base.Page( input = page_soup )

    post_soups = page.get_post_soups( )

    for j, post_soup in enumerate( post_soups ):

      post = base.Post( post_soup = post_soup)

      post_urls.append( post.post_insertion[ 'post_url' ] )

  with open( OUTPUT_FILE, 'w' ) as f:
    for post_url in post_urls:
      f.write( post_url + '\n' )

###############################################################################