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

INPUT_SOUP = 'tests/resources/thread_page.html'
INPUT_REACTION = 'tests/resources/reaction_page.html'
INPUT_USER = 'tests/resources/user_page.html'

###############################################################################

@pytest.fixture( scope = 'module' )
def resources( ):

  """SetUp fixture to create HTML resources for evaluating extraction functions.
  """

  with open( INPUT_SOUP, 'r' ) as f:
    thread_page = BeautifulSoup( f.read( ), features = 'lxml' )

  with open( INPUT_REACTION, 'r' ) as f:
    reaction_page = BeautifulSoup( f.read( ), features = 'lxml' )

  with open( INPUT_USER, 'r' ) as f:
    user_page = BeautifulSoup( f.read( ), features = 'lxml' )

  creation = functions.get_thread_creation( thread_page = thread_page )
  post = thread_page.find_all('div', {'class' : "message-inner"})[ 0 ]
  message = functions.get_post_message( post = post )
  reaction = functions.get_reaction_list( reaction_page = reaction_page )[ 0 ]

  resources_dict = dict( )

  resources_dict[ 'thread_page' ] = thread_page
  resources_dict[ 'creation' ] = creation
  resources_dict[ 'post' ] = post
  resources_dict[ 'message' ] = message
  resources_dict[ 'thread_url' ] = THREAD_URL
  resources_dict[ 'page_url' ] = THREAD_URL + 'page-2/'
  resources_dict[ 'text' ] = 'this\n is a test string...'
  resources_dict[ 'reaction_page' ] = reaction_page
  resources_dict[ 'reaction' ] = reaction
  resources_dict[ 'user_page' ] = user_page

  return resources_dict

###############################################################################