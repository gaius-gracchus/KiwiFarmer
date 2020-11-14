# -*- coding: UTF-8 -*-

"""Classes for KikiFarms forum objects
"""

###############################################################################

import requests
from bs4 import BeautifulSoup

from kiwifarmer import functions

###############################################################################

class Thread:

  """Class for initializing the scrape of a KiwiFarms thread.

  Parameters
  ----------
  thread_url : str
    URL of thread page
    e.g. ``'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'``

  """

  #---------------------------------------------------------------------------#

  def __init__( self,
    input,
    input_type = 'soup' ):

    if input_type is 'soup':

      # store parsable BeautifulSoup object as class variable
      self.soup = input

      # get thread url from soup
      self.thread_url = self.soup.find('link', {'rel' : 'canonical'})['href']

    elif input_type is 'url':

      # store page URL as class variable
      self.thread_url = input

      # make HTTP request of thread URL
      r = requests.get( self.thread_url )
      # store HTML content of HTTP request as parsable BeautifulSoup object
      self.soup = BeautifulSoup( r.content, features = 'lxml' )

    # store thread ID as class variable
    self.thread_id = functions.get_thread_id( thread_url = self.thread_url )

    # extract thread title and store as class variable
    self.thread_title = functions.get_thread_title( soup = self.soup )
    # extract thread last page and store as class variable
    self.thread_last_page = functions.get_thread_last_page( soup = self.soup )

    # extract section of HTML containing thread creation information
    self.creation = functions.get_thread_creation( soup = self.soup )

    # extract thread creator username and store as class variable
    self.thread_creator_username = functions.get_thread_creator_username( creation = self.creation )
    # extract thread creator user ID and store as class variable
    self.thread_creator_user_id = functions.get_thread_creator_user_id( creation = self.creation )
    # extract thread creation timestamp and store as class variable
    self.thread_timestamp = functions.get_thread_timestamp( creation = self.creation )

    #.........................................................................#

    # save all thread fields in a single dictionary, used for insertion into
    # MySQL database
    self.thread_insertion = {
      'thread_url' : self.thread_url,
      'thread_id' : self.thread_id,
      'thread_title' : self.thread_title,
      'last_page' : self.thread_last_page,
      'creator_username' : self.thread_creator_username,
      'creator_user_id' : self.thread_creator_user_id,
      'thread_timestamp' : self.thread_timestamp }

  #---------------------------------------------------------------------------#

  def get_pages( self ):

    """Generate a list of URLs for each page of the thread.

    Returns
    -------
    list:
      List of URLs for each page of the thread
      e,g, ``[ 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/page-2/', ]``
    """

    return [ self.thread_url + f'page-{i}/' for i in range( 1, self.thread_last_page + 1 ) ]

  #---------------------------------------------------------------------------#

###############################################################################

class Page:

  """Class for initializing the scrape of a single page in a KwiFarms thread.

  Parameters
  ----------
  page_url : str
    URL of a single page in a KiwiFarms thread
    e.g. ``'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/page-2/'``
  """

  #---------------------------------------------------------------------------#

  def __init__(self,
    input,
    input_type = 'soup' ):

    if input_type is 'soup':

      # store parsable BeautifulSoup object as class variable
      self.soup = input

    elif input_type is 'url':

      # store page URL as class variable
      self.page_url = input
      # store thread ID as class variable
      self.thread_id = functions.get_page_thread_id( page_url = self.page_url )

      # make HTTP request of page URL
      r = requests.get( self.page_url )
      # store HTML content of HTTP request as parsable BeautifulSoup object
      self.soup = BeautifulSoup( r.content, features = 'lxml' )

    else:

      msg = '`input_type` must be in `{"soup", "url"}`, and `input` must either be an instance of `bs4.element.Tag`, or `str`, respectively.'

  #---------------------------------------------------------------------------#

  def get_post_soups( self ):

    """Generate a list of BeautifulSoup HTML snippets that each contain a
    KiwiFarms post.

    Returns
    -------
    list:
      List of BeautifulSoup HTML snippets that each contain a KiwiFarms post.

    """

    return self.soup.find_all('div', {'class' : "message-inner"})

  #---------------------------------------------------------------------------#

###############################################################################

class Post:

  """Class for initializing the scrape of a single post in a KwiFarms thread.

  Parameters
  ----------
  post_soup : bs4.element.Tag
    BeautifulSoup HTML snippet that contains a KiwiFarms post

  """

  #---------------------------------------------------------------------------#

  def __init__(self,
    post_soup ):

    # store BeautifulSoup HTML snippet as class variable
    self.post = post_soup


    #.........................................................................#

    # extract section of HTML containing post message information
    message = functions.get_post_message( post = self.post )

    # extract blockquotes and blockquotes sources from message
    blockquotes_text, blockquotes_sources = functions.get_post_blockquotes( message = message )
    # extract link URLs from message
    links, links_texts = functions.get_post_links( message = message )
    # extract image URLs from message
    images = functions.get_post_images( message = message )

    # extract message text from message
    self.post_text = functions.process_text( text = message )
    message.decompose( )

    #.........................................................................#

    # store thread ID as class variable
    self.thread_id = functions.get_post_thread_id( post = self.post )
    # store post ID as class variable
    self.post_id = functions.get_post_id( post = self.post )
    # store post author username as class variable
    self.post_author_username = functions.get_post_author_username( post = self.post )
    # store post author user ID as class variable
    self.post_author_user_id = functions.get_post_author_user_id( post = self.post )
    # store post timestamp as class variable
    self.post_timestamp = functions.get_post_timestamp( post = self.post )
    # store post url as class variable
    self.post_url = functions.get_post_url( post = self.post )

    # save all post fields in a single dictionary, used for insertion into
    # MySQL database
    self.post_insertion = {
      'thread_id' : self.thread_id,
      'post_id' : self.post_id,
      'post_url' : self.post_url,
      'author_username' : self.post_author_username,
      'author_user_id' : self.post_author_user_id,
      'post_timestamp' : self.post_timestamp,
      'post_text' : self.post_text }

    # generate list of dicts for blockquote fields
    #.........................................................................#

    # initialize list for storing blockquote insertion dicts
    _blockquote_insertions = [ ]

    # loop over all blockquotes and blockquotes sources
    for bqt, bqs in zip( blockquotes_text, blockquotes_sources ):

      # create a single blockquote insertion dict
      _d = {
        'thread_id' : self.thread_id,
        'post_id' : self.post_id,
        'author_user_id' : self.post_author_user_id,
        'blockquote_text' : functions.process_text( text = bqt),
        'blockquote_source' : bqs }

      # append the blockquote insertion dict to the list of dicts
      _blockquote_insertions.append( _d )

    # save list of blockquote insertions as class variable
    self.blockquote_insertions = _blockquote_insertions

    # generate list of dicts for link fields
    #.........................................................................#

    # initialize list for storing link insertion dicts
    _link_insertions = [ ]

    # loop over all links
    for link, link_text in zip( links, links_texts ):

      if len( link ) <= 2048:

        # create a single link insertion dict
        _d = {
          'thread_id' : self.thread_id,
          'post_id' : self.post_id,
          'author_user_id' : self.post_author_user_id,
          'link_source' : link,
          'link_text' : link_text }

        # append the link insertion dict to the list of dicts
        _link_insertions.append( _d )

    # save list of link insertions as class variable
    self.link_insertions = _link_insertions

    # generate list of dicts for image fields
    #.........................................................................#

    # initialize list for storing image insertion dicts
    _image_insertions = [ ]

    # loop over all images
    for image in images:

      if len( image ) <= 2048:

        # create a single image insertion dict
        _d = {
          'thread_id' : self.thread_id,
          'post_id' : self.post_id,
          'author_user_id' : self.post_author_user_id,
          'image_source' : image }

        # append the image insertion dict to the list of dicts
        _image_insertions.append( _d )

    # save list of image insertions as class variable
    self.image_insertions = _image_insertions

    #.........................................................................#

  #---------------------------------------------------------------------------#

###############################################################################