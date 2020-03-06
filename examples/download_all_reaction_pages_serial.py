# -*- coding: UTF-8 -*-

"""Download and write to file the HTML for a lot of URLs.

Mostly taken from:
  - https://stackoverflow.com/a/56276834
  - https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

"""

###############################################################################

import os
import requests

###############################################################################

OUTPUT_DIR = '../../data/downloaded_reaction_pages'

LAST_POST_ID = 6107471

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  for i in range( 1, LAST_POST_ID + 1):

    url = f'https://kiwifarms.net/posts/{i}/reactions?reaction_id=0&list_only=1&page=1'

    r = requests.get( url )

    with open( os.path.join( OUTPUT_DIR, url[28:-43] + '.html'), 'wb') as f:
      f.write( r.content )


  # asyncio.run( main( ) )

###############################################################################