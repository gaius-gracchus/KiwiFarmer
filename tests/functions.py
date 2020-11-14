# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.functions module
"""

###############################################################################

import os
import unittest

from bs4 import BeautifulSoup

from kiwifarmer import functions

###############################################################################

class BaseTest( unittest.TestCase ):

  """Base test class containing setUp method.
  """

  #---------------------------------------------------------------------------#

  def setUp( self ):

    RESOURCES_DIR = os.path.join(
      os.path.dirname( os.path.abspath( __file__ ) ),
      'resources' )

    with open( os.path.join( RESOURCES_DIR, 'soup.html' ), 'r' ) as f:
      self.soup = BeautifulSoup( f.read( ), features="lxml" )

    with open( os.path.join( RESOURCES_DIR, 'creation.html' ), 'r' ) as f:
      self.creation = BeautifulSoup( f.read( ), features="lxml" )

    with open( os.path.join( RESOURCES_DIR, 'post.html' ), 'r' ) as f:
      self.post = BeautifulSoup( f.read( ), features="lxml" )

    with open( os.path.join( RESOURCES_DIR, 'message.html' ), 'r' ) as f:
      self.message = BeautifulSoup( f.read( ), features="lxml" )

    self.thread_url = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'

    self.page_url = self.thread_url + 'page-2/'

    #.........................................................................#

    self.function_dict = {
      'get_thread_id' : { 'thread_url' : self.thread_url },
      'get_thread_title' : { 'soup' : self.soup },
      'get_thread_last_page' : { 'soup' : self.soup },
      'get_thread_creation' : { 'soup' : self.soup },
      'get_thread_creator_username' : { 'creation' : self.creation },
      'get_thread_creator_user_id' : { 'creation' : self.creation },
      'get_thread_timestamp' : { 'creation' : self.creation },
      'get_page_thread_id' : { 'page_url' : self.page_url },
      'get_post_thread_id' : { 'post' : self.post },
      'get_post_id' : { 'post' : self.post },
      'get_post_author_username' : { 'post' : self.post },
      'get_post_author_user_id' : { 'post' : self.post },
      'get_post_timestamp' : { 'post' : self.post },
      'get_post_url' : { 'post' : self.post },
      'get_post_message' : { 'post' : self.post },
      'get_post_links' : { 'message' : self.message },
      'get_post_blockquotes' : { 'message' : self.message },
      'get_post_images' : { 'message' : self.message },
      'process_text' : { 'text' : self.thread_url } }

  #---------------------------------------------------------------------------#

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

class MinimalInitTest( BaseTest ):

  #---------------------------------------------------------------------------#

  def test( self ):

    for function_str, kwargs in self.function_dict.items( ):

      function = eval( 'functions.' + function_str )

      with self.subTest( function_str = function_str ):

        try:
          function( **kwargs )
          # print( function_str, function( **kwargs ))

        except Exception as inst:
          self.fail(
            'Minimal initialization test raised a run-time exception: '
            + repr( inst ) )

  #---------------------------------------------------------------------------#

###############################################################################

def test_suite( ):

  """Agglomerate all the tests included in this module into a test suite.
  """

  # initialize test loader for creating test suites
  ld = unittest.TestLoader( )

  # create test suites from test cases
  suites = [
    ld.loadTestsFromTestCase( MinimalInitTest ), ]

  # return aggregated test suites
  return unittest.TestSuite( suites )

###############################################################################
