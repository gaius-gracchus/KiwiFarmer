# -*- coding: UTF-8 -*-

"""Preprocess downloaded reaction files.

For some of the downloaded reaction files, there is a Cloudflare error HTML
document  either before or after the actual reaction document.
Having multiple HTML documents within the same file causes problems when
parsing the HTML with BeautifulSoup.
This script removes the unnecessary Cloudflare error HTML document.

"""

###############################################################################

import os

from bs4 import BeautifulSoup

###############################################################################

INPUT_DIR = '../../data_fresh/downloaded_pages/'

DECLARATION = '<!DOCTYPE html>'

###############################################################################

if __name__ == '__main__':

  files = sorted( os.listdir( INPUT_DIR ) )
  files = [ os.path.join( INPUT_DIR, file ) for file in files ]

  N_files = len( files )

  for i, file in enumerate( files ):

    print( f'[ {i} / {N_files} ]')

    with open( file, 'r' ) as f:
      r = f.read( )

    docs = [ DECLARATION + s for s in r.split( DECLARATION )[ 1: ] ]

    if len( docs ) > 1:

      soups = [ BeautifulSoup( doc, features = 'lxml' ) for doc in docs ]

      for soup in soups:
        if soup.find( 'meta', {'property' : 'og:url' } ) is not None:
          with open( file, 'w', encoding = 'utf-8' ) as f:
            f.write( str( soup ) )

###############################################################################