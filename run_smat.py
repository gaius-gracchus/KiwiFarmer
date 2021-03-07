# -*- coding: UTF-8 -*-

# Ingest all new KiwiFarms posts into an Elasticsearch index

###############################################################################

from datetime import datetime

from bs4 import BeautifulSoup
import requests

import redis
from elasticsearch import Elasticsearch

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

###############################################################################

def get_page_url( thread_unique, page ):

  """Convert a `thread_unique` string and a page number to the corresponding
  KiwiFarms URL.
  """

  return f'https://kiwifarms.net/threads/{thread_unique}/page-{page}'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def process_thread( thread_unique, rdb, es ):

  """Process all posts in the thread corresponding to the specified `thread_unique` and index using an Elasticsearch index.

  Parameters
  ----------
  thread_unique : str
    Section of KiwiFarms thread URL that uniquely defines a single thread.
    e.g. ``'music-suggestion-i-need-some-shit.86136'``
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
  thread_page = BeautifulSoup( r.content, features = 'lxml' )
  new_last_page = kiwifarmer.functions.get_thread_last_page( thread_page )

  # Initialize list of post timestamps, for updating the last modified datetime
  post_timestamps = list( )

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

      # Use the post ID number as the Elasticsearch index
      _id = doc.pop( 'post_id' )

      # Index the post
      res = es.index( index = ES_INDEX, id = _id, body = doc )

      # append the datetime of the post to the list of post datetimes
      post_timestamps.append( doc[ 'post_datetime' ] )

  # Define Redis hash corresponding to the thread (stores the last modified
  # datetime and the updated last page of the thread)
  mapping = {
    'last_mod' : max( post_timestamps ).isoformat( ),
    'last_page' : new_last_page }

  # Store the data corresponding to the thread in the Redis database
  rdb.hset( name = thread_unique, mapping = mapping)

###############################################################################

# Connect to Redis database and Elasticsearch instance
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Connect to Redis database using specified host, port, and database number
rdb = redis.Redis(
  host = REDIS_HOST,
  port = REDIS_PORT,
  db = REDIS_DB )

# Connect to Elasticsearch instance using specified list of hosts
es = Elasticsearch(
  hosts = ES_HOSTS )

# Get list of all URLs and their last modified date in the site's sitemap
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

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
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Initialize list of threads that have not been processed, or have been updated
# since the last time they were processed
threads_to_process = list( )

# Loop over all url objects corresponding to threads
for url in thread_urls:

  # Extract the unique identifier for the given thread
  thread_unique = url.find( 'loc' ).text.split( '/' )[ -2 ]

  # Extract the last modified datetime for the given thread
  last_mod = url.find( 'lastmod' ).text

  # If the given thread hasn't been processed, add it to the list of threads to
  # process
  if not rdb.exists( thread_unique ):

    threads_to_process.append( thread_unique )

  # If the given thread has been updated since the last time it was processed,
  # add it to the list of threads to processed
  else:

    prev_last_mod = rdb.hget( thread_unique, 'last_mod' ).decode( 'utf-8' )

    if datetime.fromisoformat( prev_last_mod ) < datetime.fromisoformat( last_mod ):

      threads_to_process.append( thread_unique )

# Process all threads that need to be ingested
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

# Loop over all threads that need to be processed
for thread_unique in threads_to_process:

  print( thread_unique )

  # Using the Redis database as a cache, find all posts in the given thread, index their data to an Elasticsearch instance
  process_thread(
    thread_unique = thread_unique,
    rdb = rdb,
    es = es )

###############################################################################