# -*- coding: UTF-8 -*-

"""Download all user pages
"""

###############################################################################

import os
import asyncio

import aiofiles
from aiohttp import ClientSession
from bs4 import BeautifulSoup

from kiwifarmer.utils import (
  page_filename_to_url,
  page_url_to_filename,
  download_many_files, )

###############################################################################

MEMBER_LIST_FILE = '../../data_20210224/member_url_list.txt'

OUTPUT_DIR = '../../data_20210224/downloaded_members/'

USERNAME = os.getenv( 'KIWIFARMS_USERNAME' )
PASSWORD = os.getenv( 'KIWIFARMS_PASSWORD' )

OUTPUT_FILE = '../../member_test.html'

SEMAPHORE = 20

THRESHOLD_KB = 20

###############################################################################

async def main( ):

  async with ClientSession( ) as session:

    async with session.get( "https://kiwifarms.net/login/login" ) as r:

      r_text = await r.read( )

    soup = BeautifulSoup( r_text.decode( 'utf-8' ), 'html.parser' )

    token = soup.find( 'input', { 'name': '_xfToken' } ).get( 'value' )

    data = {
      'username': USERNAME,
      'password': PASSWORD,
      'remember': '1',
      '_xfRedirect': '/',
      '_xfToken': token }

    await session.post( 'https://kiwifarms.net/login/login', data = data )

    await download_many_files(
      url_list = member_list,
      output_dir = OUTPUT_DIR,
      semaphore = SEMAPHORE,
      threshold_kb = THRESHOLD_KB,
      filename_to_url = page_filename_to_url,
      url_to_filename = page_url_to_filename,
      session = session )

###############################################################################

with open( MEMBER_LIST_FILE, 'r' ) as f:
  member_list = f.read( ).split( '\n' )

asyncio.run( main( ) )

###############################################################################