# -*- coding: UTF-8 -*-

# Ingest all new KiwiFarms posts into an Elasticsearch index

###############################################################################

from datetime import datetime as dt

from bs4 import BeautifulSoup
import requests

import redis
import elasticsearch

import kiwifarmer

###############################################################################

# Master sitemap for KiwiFarms
SITEMAP_URL = 'https://kiwifarms.net/sitemap.xml'

# Pattern for KiwiFarms thread URLs
THREAD_PATTERN = 'https://kiwifarms.net/threads/'

# Redis instance host
REDIS_HOST = 'localhost'
# Redis instance port number
REDIS_PORT = 6379
# Redis instance database number
REDIS_DB = 1

# List of hosts for Elasticsearch instance
ES_HOSTS = [ { 'host' : 'localhost','port' : 9200 }, ]
# Name of Elasticsearch index to store data in
ES_INDEX = 'kf_posts'

# If thread HTML contains this string, it's been deleted, and contains no posts
DELETED_THREAD_STRING = \
  'Something went wrong. Please try again or contact the administrator.'

###############################################################################

def get_page_url( thread_unique, page ):

  """Convert a `thread_unique` string and a page number to the corresponding
  KiwiFarms URL.
  """

  return f'https://kiwifarms.net/threads/{thread_unique}/page-{page}'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_threads_to_process( rdb, es ):

  """Get list of all thread unique strings and their last modified date from the
  sitemap, corresponding to threads that have been added or modified since the
  last time script was run.

  Parameters
  ----------
  rdb : redis.Redis instance
    Redis database used for caching
  es : elasticsearch.Elasticsearch instance
    Elasticsearch instance for indexing data

  """

  # Get list of all sub-sitemap URLS contained in the main KiwiFarms sitemap
  r = requests.get( SITEMAP_URL )
  soup = BeautifulSoup( r.content, features = 'lxml' )
  locs = soup.find_all( 'loc' )
  sub_sitemap_urls = [ loc.text for loc in locs ]

  # Initialize list to store all thread url objects from all sitemaps
  thread_urls = list( )

  # Loop over all sub-sitemaps
  for sub_sitemap_url in sub_sitemap_urls:

    # Parse HTML of sub-sitemap, get list of all url objects in the sub-sitemap
    r = requests.get( sub_sitemap_url )
    soup = BeautifulSoup( r.content, features = 'lxml' )
    all_urls = soup.find_all( 'url' )

    # Only include url objects that refer to a KiwiFarms thread
    _thread_urls = [ url for url in all_urls if \
      url.find( 'loc' ).text.startswith( THREAD_PATTERN ) ]

    # Store thread url objects from the sitemap in the list for all sitemaps
    thread_urls.extend( _thread_urls )

  # Get list of all threads that have not been ingested, or have new posts
  # since the last ingest
  #---------------------------------------------------------------------------#

  # Initialize list of threads that have not been processed, or have been
  # updated since the last time they were processed
  threads_to_process = dict( )

  # Loop over all url objects corresponding to threads
  for url in thread_urls:

    # Extract the unique identifier for the given thread
    thread_unique = url.find( 'loc' ).text.split( '/' )[ -2 ]

    # Extract the last modified datetime for the given thread
    last_mod = url.find( 'lastmod' ).text

    # If the given thread hasn't been processed, add it to the list of threads
    # to process
    if not rdb.exists( thread_unique ):

      threads_to_process[ thread_unique ] = last_mod

    # If the given thread has been updated since the last time it was processed,
    # add it to the list of threads to processed
    else:

      prev_last_mod = rdb.hget( thread_unique, 'last_mod' ).decode( 'utf-8' )

      if dt.fromisoformat( prev_last_mod ) < dt.fromisoformat( last_mod ):

        threads_to_process[ thread_unique ] = last_mod

  return threads_to_process

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def process_thread( thread_unique, last_mod, rdb, es ):

  """Process all posts in the thread corresponding to the specified
  `thread_unique` and index using an Elasticsearch index.

  Parameters
  ----------
  thread_unique : str
    Section of KiwiFarms thread URL that uniquely defines a single thread.
    e.g. ``'music-suggestion-i-need-some-shit.86136'``
  last_mod : str
    Datetime of the last time the thread was modified, in ISO-8601 format
    e.g. ``'2017-07-03T20:25:56+00:00'``
  rdb : redis.Redis instance
    Redis database used for caching
  es : elasticsearch.Elasticsearch instance
    Elasticsearch instance for indexing data

  """

  # If the thread has previously been processed, start at the previously stored
  # last page (so it doesn't re-index posts that have already been indexed),
  # otherwise start at the first page.
  if not rdb.exists( thread_unique ):
    start_page = '1'
  else:
    start_page = rdb.hget( thread_unique, 'last_page' ).decode( 'utf-8' )

  # Get the updated last page of the thread
  page_url = get_page_url( thread_unique, start_page )
  r = requests.get( page_url )

  # Check if the thread has been deleted (which would otherwise cause the
  # indexing of the posts to fail, since there are no posts )
  if DELETED_THREAD_STRING in r.text:

    # Define Redis hash corresponding to the thread (stores the last modified
    # datetime and the updated last page of the thread), for deleted thread
    mapping = {
      'last_mod' : last_mod,
      'last_page' : 0 }

    # Store the data corresponding to the deleted thread in the Redis database
    rdb.hset( name = thread_unique, mapping = mapping)

    return None

  thread_page = BeautifulSoup( r.content, features = 'lxml' )
  new_last_page = kiwifarmer.functions.get_thread_last_page( thread_page )

  subforum = kiwifarmer.functions.get_thread_subforum( thread_page )

  # Loop over all pages in the thread that haven't been fully processed
  for page in range( int( start_page ), int( new_last_page ) + 1 ):

    # Use BeautifulSoup to parse the given page in the thread
    page_url = get_page_url( thread_unique, page )
    r = requests.get( page_url )
    thread_page = BeautifulSoup( r.content, features = 'lxml' )

    # Get list of all HTML snippets of posts in the thread
    page = kiwifarmer.base.Page( thread_page )
    post_soups = page.get_post_soups( )

    # Loop over all posts in the given page
    for post_soup in post_soups:

      # Extract relevant data fields from the post
      post = kiwifarmer.base.Post( post = post_soup )

      # Get a dict containing relevant data fields from the post, to be used as
      # a document for the Elasticsearch index.
      doc = post.post_es_document

      # insert subforum path as field in document
      doc[ 'subforum' ] = subforum

      # Use the post ID number as the Elasticsearch index
      _id = doc.pop( 'post_id' )

      # Index the post
      es.index( index = ES_INDEX, id = _id, body = doc )

  # Define Redis hash corresponding to the thread (stores the last modified
  # datetime and the updated last page of the thread)
  mapping = {
    'last_mod' : last_mod,
    'last_page' : new_last_page }

  # Store the data corresponding to the thread in the Redis database
  rdb.hset( name = thread_unique, mapping = mapping)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def ingest( ):

  """Ingest KiwiFarms posts into Elasticsearch instance
  """

  # Connect to Redis database using specified host, port, and database number
  rdb = redis.Redis(
    host = REDIS_HOST,
    port = REDIS_PORT,
    db = REDIS_DB )

  # Connect to Elasticsearch instance using specified list of hosts
  es = elasticsearch.Elasticsearch(
    hosts = ES_HOSTS )

  # Process all threads that need to be ingested
  #---------------------------------------------------------------------------#

  threads_to_process = get_threads_to_process( rdb = rdb, es = es )

  # Loop over all threads that need to be processed
  for thread_unique, last_mod in threads_to_process.items( ):

    print( thread_unique )

    # Using the Redis database as a cache, find all posts in the given thread,
    # index their data to an Elasticsearch instance
    process_thread(
      thread_unique = thread_unique,
      last_mod = last_mod,
      rdb = rdb,
      es = es )

  # Save Redis database
  rdb.bgsave( )

###############################################################################

if __name__ == '__main__':

  while True:

    try:
      ingest( )
    except Exception as e:
      print( e )

###############################################################################