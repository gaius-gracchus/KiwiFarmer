# -*- coding: UTF-8 -*-

"""Download all pages for all threads.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import requests

from kiwifarmer import base, templates

###############################################################################

OUTPUT_DIR = '../../data_20210224'
SITEMAP_URL = 'https://kiwifarms.net/sitemap.xml'

THREAD_LIST_FILENAME = 'thread_url_list.txt'

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  output_sitemap = os.path.join( OUTPUT_DIR, 'sitemap.xml' )

  os.system( f'wget {SITEMAP_URL} -O {output_sitemap}')

  with open( output_sitemap, 'r' ) as f:
    soup = BeautifulSoup( f.read( ), 'xml' )

  urls = soup.find_all('url')
  urls = [ url.find('loc').text for url in urls ]
  urls = [ url for url in urls if url.startswith( 'https://kiwifarms.net/threads/' ) ]

  output_url_list = os.path.join( OUTPUT_DIR, THREAD_LIST_FILENAME )

  with open( output_url_list, 'w' ) as f:
    for url in urls:
      f.write( url + '\n' )

###############################################################################