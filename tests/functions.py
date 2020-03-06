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

    self.function_list = [
      'get_thread_id',
      'get_thread_title',
      'get_thread_last_page',
      'get_thread_creation',
      'get_thread_creator_username',
      'get_thread_creator_user_id',
      'get_thread_timestamp',
      'get_page_thread_id',
      'get_post_thread_id',
      'get_post_id',
      'get_post_author_username',
      'get_post_author_user_id',
      'get_post_timestamp',
      'get_post_message',
      'get_post_links',
      'get_post_blockquotes',
      'get_post_images',
      'process_text' ]

    self.kwarg_list = [
      { 'thread_url' : self.thread_url },
      { 'soup' : self.soup },
      { 'soup' : self.soup },
      { 'soup' : self.soup },
      { 'creation' : self.creation },
      { 'creation' : self.creation },
      { 'creation' : self.creation },
      { 'page_url' : self.page_url },
      { 'post' : self.post },
      { 'post' : self.post },
      { 'post' : self.post },
      { 'post' : self.post },
      { 'post' : self.post },
      { 'post' : self.post },
      { 'message' : self.message },
      { 'message' : self.message },
      { 'message' : self.message },
      { 'text' : self.thread_url } ]

  #---------------------------------------------------------------------------#

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

class MinimalInitTest( BaseTest ):

  #---------------------------------------------------------------------------#

  def test( self ):

    for function_str, kwargs in zip( self.function_list, self.kwarg_list ):

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
