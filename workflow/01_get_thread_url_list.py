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

SITEMAPS = [
  'sitemap-1.xml',
  'sitemap-2.xml' ]

URL_PREFIX = 'https://kiwifarms.net/'

THREAD_PATTERN = 'https://kiwifarms.net/threads/'
MEMBER_PATTERN = 'https://kiwifarms.net/members/'

THREAD_LIST_FILENAME = 'thread_url_list.txt'
MEMBER_LIST_FILENAME = 'member_url_list.txt'

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  for sitemap in SITEMAPS:

    output_sitemap = os.path.join( OUTPUT_DIR, sitemap )

    os.system( f'wget {URL_PREFIX + sitemap} -O {output_sitemap}')

    with open( output_sitemap, 'r' ) as f:
      soup = BeautifulSoup( f.read( ), 'xml' )

    urls = soup.find_all('url')
    urls = [ url.find('loc').text for url in urls ]

    thread_urls = [ url for url in urls if url.startswith( THREAD_PATTERN ) ]
    member_urls = [ url for url in urls if url.startswith( MEMBER_PATTERN ) ]

    thread_url_list = os.path.join( OUTPUT_DIR, THREAD_LIST_FILENAME )

    with open( thread_url_list, 'a' ) as f:
      for url in thread_urls:
        f.write( url + '\n' )

    member_url_list = os.path.join( OUTPUT_DIR, MEMBER_LIST_FILENAME )

    with open( member_url_list, 'a' ) as f:
      for url in member_urls:
        f.write( url + '\n' )

###############################################################################