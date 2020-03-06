# -*- coding: UTF-8 -*-

###############################################################################

import os

###############################################################################

OUTPUT_DIR = 'downloaded_pages'

URL_LIST_FILE = 'all_page_urls.txt'

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  with open( URL_LIST_FILE, 'r' ) as f:
    urls = f.read().split('\n')

  dirs = [ url.split( '/' )[ -3 ] for url in urls ]

  for dir in dirs:
    os.makedirs( os.path.join( OUTPUT_DIR, dir ), exist_ok = True )

###############################################################################