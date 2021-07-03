# -*- coding: UTF-8 -*-

"""Get reaction pages for posts with more than one page of reactions
"""

###############################################################################

import os
import asyncio

from bs4 import BeautifulSoup
import pandas as pd
import mysql.connector

from kiwifarmer.utils import (
  reaction_filename_to_url,
  reaction_url_to_filename,
  download_many_files, )
from kiwifarmer import base, templates

###############################################################################

SEMAPHORE = 20

THRESHOLD_KB = 15

URL_PATTERN = 'https://kiwifarms.net/posts/{}/reactions?reaction_id=0&list_only=1&page={}'

COMMAND = 'SELECT * FROM reactions'

DATABASE = 'kiwifarms_20210224'

START = 0

###############################################################################

def process_reaction_page( page_file, output_dir, cursor ):

  with open( os.path.join( output_dir, page_file ), 'r' ) as f:

    _reaction_page = BeautifulSoup( f.read( ), 'lxml' )

  reaction_page = base.ReactionPage( reaction_page = _reaction_page )

  reaction_soups = reaction_page.get_reaction_soups( )

  post_id = reaction_page.post_id

  for j, reaction in enumerate( reaction_soups ):

    reaction = base.Reaction( reaction = reaction, post_id = post_id )

    cursor.execute(templates.ADD_REACTION, reaction.reaction_insertion )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def get_url_list( page ):

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = DATABASE,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True )

  _rdf = pd.read_sql(
    sql = COMMAND,
    con = cnx )

  cnx.close( )

  rdf = _rdf.drop_duplicates( )

  d = rdf.groupby( 'post_id' )[ 'post_id' ].agg( 'count' )
  rerun = [ post_id for post_id, count in d.items( ) if count >= ( page * 50 ) ]
  urls = [ URL_PATTERN.format( post_id, page + 1 ) for post_id in rerun ]

  return urls

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def run( page ):

  output_dir = f'../../data_20210224/downloaded_reactions/page_{page + 1}'

  url_list = get_url_list( page )

  asyncio.run( download_many_files(
    url_list = url_list,
    output_dir = output_dir,
    semaphore = SEMAPHORE,
    threshold_kb = THRESHOLD_KB,
    filename_to_url = reaction_filename_to_url,
    url_to_filename = reaction_url_to_filename ) )

  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER' ),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = DATABASE,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True )

  cursor = cnx.cursor()

  # Process all reaction pages
  #---------------------------------------------------------------------------#

  cursor = cnx.cursor()

  pages = os.listdir( output_dir )

  N_pages = len( pages )

  for i, page_file in enumerate( pages[ START: ] ):

    print( f'[ {i + START} / {N_pages} ]', page_file )

    process_reaction_page( page_file, output_dir, cursor )

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################

for page in range( 1, 20 ):

  run( page = page )

###############################################################################