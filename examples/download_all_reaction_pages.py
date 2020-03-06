# -*- coding: UTF-8 -*-

"""Download and write to file the HTML for a lot of URLs.

Mostly taken from:
  - https://stackoverflow.com/a/56276834
  - https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

"""

###############################################################################

import os
import asyncio

import aiofiles
from aiohttp import ClientSession

###############################################################################

OUTPUT_DIR = '../../data/downloaded_reaction_pages'

LAST_POST_ID = 6107471

###############################################################################

async def make_request(session, url, sem):

  async with sem:
    response = await session.request(method="GET", url=url)
    filename = os.path.join( OUTPUT_DIR, url[28:-43] + '.html' )
    async for data in response.content.iter_chunked(1024):
      async with aiofiles.open(filename, "ba") as f:
        await f.write(data)
    return filename

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

async def main():

  sem = asyncio.Semaphore( 10 )

  async with ClientSession() as session:
    coros = [ make_request( session, url, sem ) for url in urls ]
    result_files = await asyncio.gather(*coros)

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  urls = [ f'https://kiwifarms.net/posts/{i}/reactions?reaction_id=0&list_only=1&page=1' for i in range( 1, LAST_POST_ID + 1 ) ]
  print( 'completed creating url list' )

  asyncio.run( main( ) )

###############################################################################