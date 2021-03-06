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

SITEMAP_URL = 'https://kiwifarms.net/sitemap.xml'
THREAD_PATTERN = 'https://kiwifarms.net/threads/'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

ES_HOSTS = [ { 'host' : 'localhost','port' : 9200 }, ]
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

  if not rdb.exists( thread_unique ):
    start_page = '1'
  else:
    start_page = rdb.hget( thread_unique, 'last_page' ).decode( 'utf-8' )

  page_url = get_page_url( thread_unique, start_page )
  r = requests.get( page_url )
  thread_page = BeautifulSoup( r.content, features = 'lxml' )

  new_last_page = kiwifarmer.functions.get_thread_last_page( thread_page )

  post_ids = list( )
  post_timestamps = list( )

  for page in range( int( start_page ), int( new_last_page ) + 1 ):

    page_url = get_page_url( thread_unique, page )
    r = requests.get( page_url )
    thread_page = BeautifulSoup( r.content, features = 'lxml' )

    page = kiwifarmer.base.Page( thread_page )

    post_soups = page.get_post_soups( )

    for post_soup in post_soups:

      post = kiwifarmer.base.Post( post = post_soup )

      doc = post.post_es_document
      _id = doc.pop( 'post_id' )

      res = es.index( index = ES_INDEX, id = _id, body = doc )

      post_ids.append( _id )
      post_timestamps.append( doc[ 'post_datetime' ] )

  mapping = {
    'last_mod' : max( post_timestamps ).isoformat( ),
    'last_page' : new_last_page,
    'last_post' : max( post_ids ) }

  rdb.hset( name = thread_unique, mapping = mapping)

###############################################################################

# Connect to Redis database and Elasticsearch instance
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

rdb = redis.Redis(
  host = REDIS_HOST,
  port = REDIS_PORT,
  db = REDIS_DB )

# rdb.flushdb( )

es = Elasticsearch(
  hosts = ES_HOSTS )

# Get list of all URLs and their last modified date in the site's sitemap
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

r = requests.get( SITEMAP_URL )
soup = BeautifulSoup( r.content, features = 'lxml' )

locs = soup.find_all( 'loc' )
sub_sitemap_urls = [ loc.text for loc in locs ]

thread_urls = list( )

for sub_sitemap_url in sub_sitemap_urls:

  r = requests.get( sub_sitemap_url )
  soup = BeautifulSoup( r.content, features = 'lxml' )

  all_urls = soup.find_all( 'url' )

  _thread_urls = [ url for url in all_urls if \
    url.find( 'loc' ).text.startswith( THREAD_PATTERN ) ]

  thread_urls.extend( _thread_urls )

threads_to_process = list( )

# Get list of all threads that have not been ingested, or have new posts
# since the last ingest
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

for url in thread_urls:

  thread_unique = url.find( 'loc' ).text.split( '/' )[ -2 ]
  last_mod = url.find( 'lastmod' ).text

  if not rdb.exists( thread_unique ):

    threads_to_process.append( thread_unique )

  else:

    prev_last_mod = rdb.hget( thread_unique, 'last_mod' ).decode( 'utf-8' )

    if datetime.fromisoformat( prev_last_mod ) < datetime.fromisoformat( last_mod ):

      threads_to_process.append( thread_unique )

# Process all threads that need to be ingested
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

for thread_unique in threads_to_process:

  print( thread_unique )

  process_thread(
    thread_unique = thread_unique,
    rdb = rdb,
    es = es )

###############################################################################