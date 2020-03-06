# -*- coding: UTF-8 -*-

"""Download all pages for all threads.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import requests

from kiwifarmer import base, templates

###############################################################################

OUTPUT_DIR = 'downloaded'
SITEMAP_URL = 'https://kiwifarms.net/sitemap.xml'

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  os.system( f'wget {SITEMAP_URL}')

  with open( 'sitemap.xml', 'r' ) as f:
    soup = BeautifulSoup( f.read( ), 'xml' )

  urls = soup.find_all('url')
  urls = [ url.find('loc').text for url in urls ]
  urls = [ url for url in urls if url.startswith( 'https://kiwifarms.net/threads/' ) ]

  with open( 'url_list.txt', 'w' ) as f:
    for url in urls:
      f.write( url + '\n' )

###############################################################################