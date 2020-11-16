# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.utils module

The full set of tests for this module can be evaluated by executing the
command::

  $ python -m pytest tests/utils.py

from the project root directory.

"""
###############################################################################

import tempfile
import asyncio

import aiofiles
from aiohttp import ClientSession
import pytest

from kiwifarmer import (
  utils )

###############################################################################

PAGE_URL = 'https://kiwifarms.net/threads/john-cameron-denton-atomwaffen-division-siegeculture.38120/page-1/'

PAGE_FILENAME = 'john-cameron-denton-atomwaffen-division-siegeculture.38120_page-1.html'

REACTION_URL = 'https://kiwifarms.net/posts/1234/reactions?reaction_id=0&list_only=1&page=1'

REACTION_FILENAME = '1234_page-1.html'

URL_LIST = [ 'https://example.com', 'https://example.net' ]

# page conversion utility functions
###############################################################################

def test_minimal_init_page_filename_to_url( ):

  utils.page_filename_to_url( filename = PAGE_FILENAME )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_minimal_init_page_url_to_filename( ):

  utils.page_url_to_filename( url = PAGE_URL )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_page_url_to_filename_to_url( ):

  assert utils.page_filename_to_url(
    filename = utils.page_url_to_filename( url = PAGE_URL ) ) == PAGE_URL

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_page_filename_to_url_to_filename( ):

  assert utils.page_url_to_filename(
    url = utils.page_filename_to_url( filename = PAGE_FILENAME ) ) == PAGE_FILENAME

# reaction conversion utility functions
###############################################################################

def test_minimal_init_reaction_filename_to_url( ):

  utils.reaction_filename_to_url( filename = REACTION_FILENAME )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_minimal_init_reaction_url_to_filename( ):

  utils.reaction_url_to_filename( url = REACTION_URL )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_reaction_url_to_filename_to_url( ):

  assert utils.reaction_filename_to_url(
    filename = utils.reaction_url_to_filename( url = REACTION_URL ) ) == REACTION_URL

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_reaction_filename_to_url_to_filename( ):

  assert utils.reaction_url_to_filename(
    url = utils.reaction_filename_to_url( filename = REACTION_FILENAME ) ) == REACTION_FILENAME

# file downloading utility functions
###############################################################################

@pytest.mark.asyncio
async def test_make_request( ):

  url_to_filename = lambda url : url.split( '/' )[ -1 ][ : -4 ] + 'html'

  with tempfile.TemporaryDirectory() as temp_dir:

    async with ClientSession( ) as session:

      sem = asyncio.Semaphore( 2 )

      await utils.make_request(
        session = session,
        url = URL_LIST[ 0 ],
        sem = sem,
        output_dir = temp_dir,
        url_to_filename = url_to_filename, )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

@pytest.mark.asyncio
async def test_download_many_files( ):

  url_to_filename = lambda url : url.split( '/' )[ -1 ][ : -4 ] + 'html'
  filename_to_url = lambda filename : 'https://www.' + filename.split( '.' )[ 0 ][ : -4 ] + '.com'

  with tempfile.TemporaryDirectory() as temp_dir:
    await utils.download_many_files(
      url_list = URL_LIST,
      output_dir = temp_dir,
      semaphore = 2,
      threshold_kb = 0,
      url_to_filename = url_to_filename,
      filename_to_url = filename_to_url )

###############################################################################