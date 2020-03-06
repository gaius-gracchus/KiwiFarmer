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

  os.makedirs( OUTPUT_DIR )

  os.system( f'wget {SITEMAP_URL}')

  with open( 'sitemap.xml', 'r' ) as f:
    soup = BeautifulSoup( f.read( ), 'xml' )

  urls = soup.find_all('url')
  urls = [ url.find('loc').text for url in urls ]
  urls = [ url for url in urls if url.startswith( 'https://kiwifarms.net/threads/' ) ]

  for thread_url in urls:

    try:

      output_thread_dir = os.path.join( OUTPUT_DIR, thread_url[30:-1] )
      os.makedirs( output_thread_dir, exist_ok = True )

      thread = base.Thread( thread_url = thread_url )
      page_urls = thread.get_pages( )

      for page_url in page_urls:

        r = requests.get( page_url )
        page_soup = BeautifulSoup( r.content, 'lxml' )

        output_page_filename = page_url.split('/')[-2] + '.html'

        with open( os.path.join( output_thread_dir, output_page_filename ), 'w' ) as f:
          f.write( str( page_soup ) )

    except:
      with open( 'url_download_errors.csv', 'a' ) as f:
        f.write( thread_url  + '\n' )

###############################################################################