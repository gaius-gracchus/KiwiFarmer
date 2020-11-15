# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.functions module
"""

###############################################################################

import os
import pytest

from bs4 import BeautifulSoup

from kiwifarmer import functions

###############################################################################

KWARG_DICT = {
  'get_thread_id' : 'thread_url',
  'get_thread_title' : 'soup',
  'get_thread_last_page' : 'soup',
  'get_thread_creation' : 'soup',
  'get_thread_creator_username' : 'creation',
  'get_thread_creator_user_id' : 'creation',
  'get_thread_timestamp' : 'creation',
  'get_page_thread_id' : 'page_url',
  'get_post_thread_id' : 'post',
  'get_post_id' : 'post',
  'get_post_author_username' : 'post',
  'get_post_author_user_id' : 'post' ,
  'get_post_timestamp' : 'post',
  'get_post_url' : 'post',
  'get_post_message' : 'post',
  'get_post_links' : 'message',
  'get_post_blockquotes' : 'message',
  'get_post_images' : 'message',
  'process_text' : 'text' }

KWARG_LIST = list( KWARG_DICT.items( ) )

###############################################################################

@pytest.fixture( scope = 'module' )
def resources( ):

  RESOURCES_DIR = os.path.join(
    os.path.dirname( os.path.abspath( __file__ ) ),
    'resources' )

  resources_dict = dict( )

  with open( os.path.join( RESOURCES_DIR, 'soup.html' ), 'r' ) as f:
    resources_dict[ 'soup' ] = BeautifulSoup( f.read( ), features="lxml" )

  with open( os.path.join( RESOURCES_DIR, 'creation.html' ), 'r' ) as f:
    resources_dict[ 'creation' ] = BeautifulSoup( f.read( ), features="lxml" )

  with open( os.path.join( RESOURCES_DIR, 'post.html' ), 'r' ) as f:
    resources_dict[ 'post' ] = BeautifulSoup( f.read( ), features="lxml" )

  with open( os.path.join( RESOURCES_DIR, 'message.html' ), 'r' ) as f:
    resources_dict[ 'message' ] = BeautifulSoup( f.read( ), features="lxml" )

  resources_dict[ 'thread_url' ] = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'

  resources_dict[ 'page_url' ] = resources_dict[ 'thread_url' ] + 'page-2/'

  resources_dict[ 'text' ] = 'this\n is a test string...'

  return resources_dict

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

@pytest.mark.parametrize( 'function_str,kwarg', KWARG_LIST )
def test_minimal_init( resources, function_str, kwarg ):

  function = eval( 'functions.' + function_str )
  kwargs = { kwarg : resources[ kwarg ]}

  function( **kwargs )

###############################################################################