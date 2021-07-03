# -*- coding: UTF-8 -*-

"""Insert reaction pages into database
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import requests

from kiwifarmer import base, templates, utils

###############################################################################

REACTION_PAGE_DIR = '../../data_20210224/downloaded_reactions'

REACTION_FILTERED_LIST = '../../data_20210224/downloaded_reactions_filtered.txt'

START = 0

DATABASE = 'kiwifarms_20210224'

###############################################################################

def process_reaction_page( page_file, cursor ):

  with open( os.path.join( REACTION_PAGE_DIR, page_file ), 'r' ) as f:

    _reaction_page = BeautifulSoup( f.read( ), 'lxml' )

  reaction_page = base.ReactionPage( reaction_page = _reaction_page )

  reaction_soups = reaction_page.get_reaction_soups( )

  post_id = reaction_page.post_id

  for j, reaction in enumerate( reaction_soups ):

    reaction = base.Reaction( reaction = reaction, post_id = post_id )

    cursor.execute(templates.ADD_REACTION, reaction.reaction_insertion )

###############################################################################

if __name__ == '__main__':

  # Connect to MySQL database
  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = DATABASE,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True )

  cursor = cnx.cursor()

  for table_name in templates.TABLES.keys( ):
    table_description = templates.TABLES[table_name]
    try:
      print("Creating table {}: ".format(table_name), end='')
      cursor.execute(table_description)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("already exists.")
      else:
        print(err.msg)
    else:
      print("OK")

  # Process HTML files of pages, insert fields into `post` table in database
  #---------------------------------------------------------------------------#

  with open( REACTION_FILTERED_LIST, 'r' ) as f:
    pages = f.read( ).split( '\n' )
  pages = list( filter( None, pages ) )

  N_pages = len( pages )

  for i, page_file in enumerate( pages[ START: ] ):

    print( f'[ {i + START} / {N_pages} ]', page_file )

    try:

      process_reaction_page( page_file, cursor )

    except Exception as e:

      print( e )

      page_url = utils.reaction_filename_to_url( page_file )
      r = requests.get( page_url )

      output_file = os.path.join( REACTION_PAGE_DIR, page_file )
      with open( output_file, 'wb' ) as f:
        f.write( r.content )

      process_reaction_page( page_file, cursor )

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################