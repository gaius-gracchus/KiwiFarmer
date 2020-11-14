# -*- coding: UTF-8 -*-

"""Utility functions.
"""

###############################################################################

import os
import asyncio

import aiofiles
from aiohttp import ClientSession

###############################################################################

def url_to_filename( url ):

  """Convert a KiwiFarms url to a unique, valid HTML file name.

  Parameters
  ----------
  url : str
    URL of a Kiwifarms forum page
    e.g. ``'https://kiwifarms.net/threads/john-cameron-denton-atomwaffen-division-siegeculture.38120/page-1/'``

  Returns
  -------
  str
    e.g. ``'john-cameron-denton-atomwaffen-division-siegeculture.38120_page-1.html'``
  """

  filename = url[ 30 : -1 ].replace('/page', '_page') + '.html'

  return filename

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def filename_to_url( filename ):

  """Convert the unique valid HTML filename (basename; doesn't include
  directory) to its corresponding KiwiFarms url.

  Parameters
  ----------
  filename : str
    unique filename of a Kiwifarms forum page
    e.g. ``'john-cameron-denton-atomwaffen-division-siegeculture.38120_page-1.html'``

  Returns
  -------
  str
    e.g. ``'https://kiwifarms.net/threads/john-cameron-denton-atomwaffen-division-siegeculture.38120/page-1/'``

  """

  url = 'https://kiwifarms.net/threads/' + filename[:-5].replace('_page','/page') + '/'

  return url

###############################################################################

async def make_request( session, url, sem, output_dir ):

  """Asynchronous function to download a single URL and save the resulting HTML file in a specified output directory.

  Parameters
  ----------
  session : aiohttp.ClientSession( )
    Interface for making multiple requests
  url : str
    URL to download
  sem : asyncio.Semaphore
    Semaphore used for asynchronous requests
  output_dir : str
    Directory to save HTML files to

  Returns
  -------
  str :
    Filename of HTML file that was saved.
  """

  async with sem:
    response = await session.request( method = "GET", url = url )
    filename = os.path.join( output_dir, url_to_filename( url ) )
    async for data in response.content.iter_chunked( 1024 ):
      async with aiofiles.open( filename, "ba" ) as f:
        await f.write( data )
    return filename

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

async def download_many_files( url_list, output_dir, semaphore, threshold_kb ):

  """Asynchronous function to download, in parallel, a list of URLs, and save
  the resulting HTML files in a specified output directory.

  Parameters
  ----------
  url_list : list
    List of URLs (strings) to download
  output_dir : str
    Directory to save HTML files to
  semaphore : int
    Maximum number of active parallel connections
  threshold_kb : int
    Files below this size are assumed to have failed

  """

  os.makedirs( output_dir, exist_ok = True )

  file_list = [ url_to_filename( url ) for url in url_list ]

  threshold_b = threshold_kb * 1024

  existing_files = sorted( os.listdir( output_dir ) )

  existing_files = [
    file for file in existing_files if os.path.getsize(
      os.path.join( output_dir, file ) ) >= threshold_b ]

  files_to_download = set( file_list ) - set( existing_files )

  urls_to_download = [ filename_to_url( file ) for file in files_to_download ]

  print( f'Number of URLs to download: {len( urls_to_download )}' )

  sem = asyncio.Semaphore( semaphore )

  #---------------------------------------------------------------------------#

  async with ClientSession() as session:
    coros = [ make_request( session, url, sem, output_dir ) for url in urls_to_download ]
    result_files = await asyncio.gather( *coros )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
