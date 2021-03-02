# -*- coding: UTF-8 -*-

"""Utility functions.
"""

###############################################################################

import os
import asyncio

import aiofiles
from aiohttp import ClientSession

###############################################################################

def page_url_to_filename( url ):

  """Convert a KiwiFarms page url to a unique, valid HTML file name.

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

def page_filename_to_url( filename ):

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

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def reaction_url_to_filename( url ):

  """Convert a KiwiFarms post reaction url to a unique, valid HTML file name.

  Parameters
  ----------
  url : str
    URL of a Kiwifarms forum post reaction list
    e.g. ``'https://kiwifarms.net/posts/1234/reactions?reaction_id=0&list_only=1&page=1'``

  Returns
  -------
  str
    e.g. ``'1234_page-1.html'``
  """

  s = url.split( '/' )

  post_id = s[ 4 ]
  page = s[ -1 ].split( '=' )[ -1 ]

  filename = f'{post_id}_page-{page}.html'

  return filename

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def reaction_filename_to_url( filename ):

  """Convert the unique valid HTML filename (basename; doesn't include
  directory) to its corresponding KiwiFarms url.

  Parameters
  ----------
  filename : str
    unique filename of a Kiwifarms post reaction list
    e.g. ``'1234_page-1.html'``

  Returns
  -------
  str
    e.g. ``'https://kiwifarms.net/posts/1234/reactions?reaction_id=0&list_only=1&page=1'``

  """

  s = filename.split( '_' )

  post_id = s[ 0 ]
  page = s[ -1 ][ 5 : -5 ]

  url = f'https://kiwifarms.net/posts/{post_id}/reactions?reaction_id=0&list_only=1&page={page}'

  return url

###############################################################################

def string_to_int( s ):

  """Convert a string representation of a number to an integer

  Parameters
  ----------
  s : bs4.element.Tag
    BeautifulSoup representation of a number.
    e.g. ``'21,564'``

  Returns
  -------
  int
    Integer representation of the number.
    e.g. ``21564``

  """

  return int( s.text.strip( '\n' ).replace( ',', '' ) )

###############################################################################

def get_bad_files(
  output_dir,
  pattern = '</html>\n' ):

  """Find all files that aren't complete HTML documents

  Parameters
  ----------
  output_dir : str
    Directory in which to search for malformed HTML files
  pattern : str
    If the last line of the file doesn't contain this string, the file is considered "bad" (i.e. a malformed HTML file)

  Returns
  -------
  bad_files : list of str
    List of malformed HTML files

  """

  files = os.listdir( output_dir )

  bad_files = list( )

  for file in files:

    with open( os.path.join( output_dir, file ), 'rb' ) as f:

      f.seek(-2, os.SEEK_END)

      while f.read(1) != b'\n':
          f.seek(-2, os.SEEK_CUR)
      last_line = f.readline( ).decode( )

    if last_line != pattern:
      bad_files.append( file )

  return bad_files

###############################################################################

async def make_request(
  session,
  url,
  sem,
  output_dir,
  url_to_filename ):

  """Asynchronous function to download a single URL and save the resulting HTML
  file in a specified output directory.

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
  url_to_filename : callable
    Function to convert a URL to an HTML filename

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

async def download_many_files(
  url_list,
  output_dir,
  semaphore,
  threshold_kb,
  url_to_filename,
  filename_to_url,
  session = None, ):

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
  url_to_filename : callable
    Function to convert a URL to an HTML filename
  filename_to_url : callable
    Function to convert an HTML filename to a URL

  """

  # Create output directory to store HTML files of threads, if the directory
  # doesn't already exist
  os.makedirs( output_dir, exist_ok = True )

  # Convert file size threshold from kilobytes to bytes
  threshold_b = threshold_kb * 1024

  # Initialize variable for number of files left to download
  N_files_to_download = 1

  # Keep running until all files are downloaded
  while N_files_to_download > 0:

    # Get list of all files in the list of URLs
    file_list = [ url_to_filename( url ) for url in url_list ]

    # Get list of all files in the output directory
    _files = sorted( os.listdir( output_dir ) )

    bad_files = get_bad_files(
      output_dir = output_dir, )

    # Delete all files in the output directory smaller than the threshold size
    [ os.remove( os.path.join( output_dir, file ) ) for file in _files if os.path.getsize( os.path.join( output_dir, file ) ) <= threshold_b ]

    # Delete all malformed HTML files in the output directory
    [ os.remove( os.path.join( output_dir, file ) ) for file in bad_files ]

    # Get list of all files in the output directory, not including the ones
    # just deleted for being too small
    files = sorted( os.listdir( output_dir ) )

    # Get a list of all files that still need to be downloaded
    files_to_download = set( file_list ) - set( files )

    # Compute the number of files left to download (function stops when this
    # value is zero)
    N_files_to_download = len( files_to_download )

    # Convert filename to URL, for all files to be downloaded
    urls_to_download = [ filename_to_url( file ) for file in files_to_download ]

    print( f'Number of URLs to download: {N_files_to_download}' )

    # Initialize asynchronous semaphore (higher values download more files at a
    # time, but typically leads to more response error codes)
    sem = asyncio.Semaphore( semaphore )

    #-------------------------------------------------------------------------#

    # Use aiohttp to download all the URLs and save them as HTML files
    async with ClientSession( ) as session:
      coros = [ make_request( session, url, sem, output_dir, url_to_filename ) for url in urls_to_download ]
      result_files = await asyncio.gather( *coros )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#