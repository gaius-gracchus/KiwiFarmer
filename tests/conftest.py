# -*- coding: UTF-8 -*-

"""Configuration for pytest sessions
"""

###############################################################################

import pytest

import requests
from bs4 import BeautifulSoup

from kiwifarmer import functions

###############################################################################

THREAD_URL = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'

INPUT_SOUP = 'tests/resources/soup.html'

###############################################################################

@pytest.fixture( scope = 'module' )
def resources( ):

  """SetUp fixture to create HTML resources for evaluating extraction functions.
  """

  with open( INPUT_SOUP, 'r' ) as f:
    soup = BeautifulSoup( f.read( ), features = 'lxml' )

  creation = functions.get_thread_creation( soup = soup )
  post = soup.find_all('div', {'class' : "message-inner"})[ 0 ]
  # print( 'POST IN FIXTURE', post)

  message = functions.get_post_message( post )

  resources_dict = dict( )

  resources_dict[ 'soup' ] = soup
  resources_dict[ 'creation' ] = creation
  resources_dict[ 'post' ] = post
  resources_dict[ 'message' ] = message
  resources_dict[ 'thread_url' ] = THREAD_URL
  resources_dict[ 'page_url' ] = THREAD_URL + 'page-2/'
  resources_dict[ 'text' ] = 'this\n is a test string...'

  return resources_dict

###############################################################################