# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.functions module
"""

###############################################################################

import os

import pytest
import requests
from bs4 import BeautifulSoup

from kiwifarmer import functions

###############################################################################

THREAD_URL = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'

KWARG_LIST = [
  ( 'get_thread_id', 'thread_url' ),
  ( 'get_thread_title', 'soup' ),
  ( 'get_thread_last_page', 'soup' ),
  ( 'get_thread_creation', 'soup' ),
  ( 'get_thread_creator_username', 'creation' ),
  ( 'get_thread_creator_user_id', 'creation' ),
  ( 'get_thread_timestamp', 'creation' ),
  ( 'get_page_thread_id', 'page_url' ),
  ( 'get_post_thread_id', 'post' ),
  ( 'get_post_id', 'post' ),
  ( 'get_post_author_username', 'post' ),
  ( 'get_post_author_user_id', 'post'  ),
  ( 'get_post_timestamp', 'post' ),
  ( 'get_post_url', 'post' ),
  ( 'get_post_message', 'post' ),
  ( 'get_post_links', 'message' ),
  ( 'get_post_blockquotes', 'message' ),
  ( 'get_post_images', 'message' ),
  ( 'process_text', 'text' ) ]

###############################################################################

@pytest.fixture( scope = 'module' )
def resources( ):

  """SetUp fixture to create HTML resources for evaluating extraction functions.
  """

  r = requests.get( THREAD_URL )

  soup = BeautifulSoup( r.content, features = "lxml" )
  creation = functions.get_thread_creation( soup = soup )
  post = soup.find_all('div', {'class' : "message-inner"})[ 0 ]
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

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

@pytest.mark.parametrize( 'function_str,kwarg', KWARG_LIST )
def test_minimal_init( resources, function_str, kwarg ):

  function = eval( 'functions.' + function_str )
  kwargs = { kwarg : resources[ kwarg ]}

  function( **kwargs )

###############################################################################