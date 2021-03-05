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

THREAD_URL = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'
REACTION_URL = 'https://kiwifarms.net/posts/2924919/reactions?reaction_id=0&list_only=1&page=1'
USER_URL = 'https://kiwifarms.net/members/magnum-dong.9983/'
USER_ABOUT_URL = 'https://kiwifarms.net/members/magnum-dong.9983/about'
USER_FOLLOWING_URL = 'https://kiwifarms.net/members/234/following/page-1'

###############################################################################

@pytest.fixture( scope = 'module' )
def resources( ):

  """SetUp fixture to create HTML resources for evaluating extraction functions.
  """

  r = requests.get( THREAD_URL )
  thread_page = BeautifulSoup( r.content, features = "lxml" )

  r = requests.get( REACTION_URL )
  reaction_page = BeautifulSoup( r.content, features = "lxml" )

  r = requests.get( USER_URL )
  user_page = BeautifulSoup( r.content, features = "lxml" )

  r = requests.get( USER_ABOUT_URL )
  user_about_page = BeautifulSoup( r.content, features = "lxml" )

  r = requests.get( USER_FOLLOWING_URL )
  following_page = BeautifulSoup( r.content, features = "lxml" )

  creation = functions.get_thread_creation( thread_page = thread_page )
  post = thread_page.find_all('div', {'class' : "message-inner"})[ 0 ]
  message = functions.get_post_message( post = post )
  reaction = functions.get_reaction_list( reaction_page = reaction_page )[ 0 ]
  trophy = user_about_page.find( 'li', { 'class' : 'block-row' } )
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
  resources_dict[ 'user_about_page' ] = user_about_page
  resources_dict[ 'trophy' ] = trophy
  resources_dict[ 'following_page' ] = following_page

  return resources_dict

###############################################################################