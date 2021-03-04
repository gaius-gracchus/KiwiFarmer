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
    thread_page, ):

    # store parsable BeautifulSoup object as class variable
    self.thread_page = thread_page

    # get thread url from soup
    self.thread_url = self.thread_page.find('link', {'rel' : 'canonical'})['href']

    # store thread ID as class variable
    self.thread_id = functions.get_thread_id( thread_url = self.thread_url )

    # extract thread title and store as class variable
    self.thread_title = functions.get_thread_title( thread_page = self.thread_page )
    # extract thread last page and store as class variable
    self.thread_last_page = functions.get_thread_last_page( thread_page = self.thread_page )

    # extract section of HTML containing thread creation information
    self.creation = functions.get_thread_creation( thread_page = self.thread_page )

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

  def __init__( self,
    thread_page,):

    # store parsable BeautifulSoup object as class variable
    self.thread_page = thread_page

  #---------------------------------------------------------------------------#

  def get_post_soups( self ):

    """Generate a list of BeautifulSoup HTML snippets that each contain a
    KiwiFarms post.

    Returns
    -------
    list:
      List of BeautifulSoup HTML snippets that each contain a KiwiFarms post.

    """

    _post_soups = self.thread_page.find_all('div', {'class' : "message-inner"})
    post_soups = [ post_soup for post_soup in _post_soups if post_soup.find('article', {'class' : 'message-body js-selectToQuote'}) ]

    return post_soups

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
    post ):

    # store BeautifulSoup HTML snippet as class variable
    self.post = post

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
        'blockquote_text' : functions.process_text( text = bqt ),
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

class ReactionPage:

  """Class for initializing the scrape of all reactions to a KwiFarms post.

  Parameters
  ----------
  soup : bs4.element.Tag
    BeautifulSoup HTML document of entire reaction page

  """

  #---------------------------------------------------------------------------#

  def __init__( self,
    reaction_page ):

    # store parsable BeautifulSoup object as class variable
    self.reaction_page = reaction_page

    url = reaction_page.find( 'meta', {'property' : 'og:url' } )[ 'content' ]
    self.post_id = int( url.split( '/' )[ 4 ] )

  #---------------------------------------------------------------------------#

  def get_reaction_soups( self ):

    """Generate a list of BeautifulSoup HTML snippets that each contain a
    KiwiFarms reaction.

    Returns
    -------
    list:
      List of BeautifulSoup HTML snippets that each contain a KiwiFarms reaction.

    """

    return functions.get_reaction_list( reaction_page = self.reaction_page )

  #---------------------------------------------------------------------------#

###############################################################################

class Reaction:

  """Class for initializing the scrape of a single reaction to a KwiFarms post.

  Parameters
  ----------
  reaction_soup : bs4.element.Tag
    BeautifulSoup HTML snippet that contains a single KiwiFarms reaction
  post_id : int
    Unique post ID number of the post the reaction is to.

  """

  #---------------------------------------------------------------------------#

  def __init__( self,
    reaction,
    post_id ):

    # store BeautifulSoup HTML snippet as class variable
    self.reaction = reaction

    # store post ID as class variable, since it's not available in the
    # individual reaction and needs to be passed from the ReactionPage class
    self.post_id = post_id

    #.........................................................................#

    # store reaction author name as class variable
    self.reaction_author_username = functions.get_reaction_author_username( reaction = self.reaction )
    # store reaction author user ID as class variable
    self.reaction_author_user_id = functions.get_reaction_author_user_id( reaction = self.reaction )
    # store reaction ID as class variable
    self.reaction_id = functions.get_reaction_id( reaction = self.reaction )
    # store reaction name as class variable
    self.reaction_name = functions.get_reaction_name( reaction = self.reaction )
    # store reaction author timestamp as class variable
    self.reaction_timestamp = functions.get_reaction_timestamp( reaction = self.reaction )

    #.........................................................................#

    # save all reaction fields in a single dictionary, used for insertion into
    # MySQL database
    self.reaction_insertion = {
      'post_id' : self.post_id,
      'author_username' : self.reaction_author_username,
      'author_user_id' : self.reaction_author_user_id,
      'reaction_id' : self.reaction_id,
      'reaction_name' : self.reaction_name,
      'reaction_timestamp' : self.reaction_timestamp }

  #---------------------------------------------------------------------------#

###############################################################################

class User:

  """Class for initializing the scrape of a single KiwiFarms user.

  Parameters
  ----------
  user_page : bs4.element.Tag
    BeautifulSoup HTML snippet that contains a KiwiFarms user page

  """

  #---------------------------------------------------------------------------#

  def __init__( self,
    user_page ):

    # store BeautifulSoup HTML document as class variable
    self.user_page = user_page

    #.........................................................................#

    # store user username as class variable
    self.user_username = functions.get_user_username( user_page = self.user_page )
    # store user ID as class variable
    self.user_id = functions.get_user_id( user_page = self.user_page )
    # store user profile picture link as class variable
    self.user_image = functions.get_user_image( user_page = self.user_page )
    # store number of user messages as class variable
    self.user_messages = functions.get_user_messages( user_page = self.user_page )
    # store user reaction score as class variable
    self.user_reaction_score = functions.get_user_reaction_score( user_page = self.user_page )
    # store number of user points as class variable
    self.user_points = functions.get_user_points( user_page = self.user_page )
    # store "Joined" and "Last Seen" timestamps as class variables
    self.user_joined, self.user_last_seen = functions.get_user_timestamps( user_page = self.user_page )

    #.........................................................................#

    # save all user fields in a single dictionary, used for insertion into
    # MySQL database
    self.user_insertion = {
      'user_username' : self.user_username,
      'user_id' : self.user_id,
      'user_image' : self.user_image,
      'user_messages' : self.user_messages,
      'user_reaction_score' : self.user_reaction_score,
      'user_points' : self.user_points,
      'user_joined' : self.user_joined,
      'user_last_seen' : self.user_last_seen, }

    #.........................................................................#

  #---------------------------------------------------------------------------#

###############################################################################

class Following:

  """Class for initializing the scrape of the following of a single KiwiFarms user.

  Parameters
  ----------
  following_page : bs4.element.Tag
    BeautifulSoup HTML snippet that contains the "Following" page of a
    KiwiFarms user

  """

  #---------------------------------------------------------------------------#

  def __init__( self,
    following_page ):

    # store BeautifulSoup HTML document as class variable
    self.following_page = following_page

    #.........................................................................#

    # store user username as class variable
    self.user_id = functions.get_following_user_id( following_page = self.following_page )
    self.following_user_ids = functions.get_following_following_ids( following_page = self.following_page )

    # generate list of dicts for following fields
    #.........................................................................#

    # initialize list for storing following insertion dicts
    _following_insertions = list( )

    # loop over all following users
    for fid in self.following_user_ids:

      _d = {
        'user_id' : self.user_id,
        'following_user_id' : fid, }

      # append the following insertion dict to the list of dicts
      _following_insertions.append( _d )

    # save list of following insertions as class variable
    self.following_insertions = _following_insertions

    #.........................................................................#

  #---------------------------------------------------------------------------#

###############################################################################