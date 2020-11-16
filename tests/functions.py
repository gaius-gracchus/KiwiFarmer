# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.functions module
"""

###############################################################################

import os

import pytest

from kiwifarmer import functions

###############################################################################

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

@pytest.mark.parametrize( 'function_str,kwarg', KWARG_LIST )
def test_minimal_init( resources, function_str, kwarg ):

  with open( kwarg + '__' + function_str + '.html', 'w' ) as f:
    f.write( str( resources[ kwarg ] ) )

  function = eval( 'functions.' + function_str )
  kwargs = { kwarg : resources[ kwarg ]}

  function( **kwargs )

###############################################################################