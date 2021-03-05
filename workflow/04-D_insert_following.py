# -*- coding: UTF-8 -*-

"""Test initialization of the `Following` class.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import base, templates

###############################################################################

PAGE_DIR = '../../data_20210224/downloaded_members_connections'

START = 0

DATABASE = 'kiwifarms_20210224'

###############################################################################

if __name__ == '__main__':


  # Connect to database
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

  # Process HTML files of pages, insert fields into `post` table in database
  #---------------------------------------------------------------------------#

  pages = os.listdir( PAGE_DIR )
  pages = [ p for p in pages if p.split( '_' )[ 1 ] == 'following' ]
  N_pages = len( pages )

  for i, page_file in enumerate( pages[ START: ] ):

    print( f'[ {i + START} / {N_pages} ]', page_file )

    with open( os.path.join( PAGE_DIR, page_file ), 'r' ) as f:

      following_page = BeautifulSoup( f.read( ), 'lxml' )

    following = base.Following( following_page = following_page )

    cursor.executemany(templates.ADD_FOLLOWING, following.following_insertions)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################