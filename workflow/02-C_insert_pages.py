# -*- coding: UTF-8 -*-

"""Test initialization of the `Thread` class.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import base, templates

###############################################################################

PAGE_DIR = '../../data_20210224/downloaded_pages'

START = 0

DATABASE = 'kiwifarms_20210224'

###############################################################################

if __name__ == '__main__':

  # Create tables in database (you only need to do this once)
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
  N_pages = len( pages )

  for i, page_file in enumerate( pages[ START: ] ):

    print( f'[ {i + START} / {N_pages} ]', page_file )

    with open( os.path.join( PAGE_DIR, page_file ), 'r' ) as f:

      thread_page = BeautifulSoup( f.read( ), 'lxml' )

    page = base.Page( thread_page = thread_page )

    post_soups = page.get_post_soups( )

    for j, post in enumerate( post_soups ):

      post = base.Post( post = post )

      cursor.execute(templates.ADD_POST, post.post_insertion)
      cursor.executemany(templates.ADD_BLOCKQUOTE, post.blockquote_insertions)
      cursor.executemany(templates.ADD_LINK, post.link_insertions)
      cursor.executemany(templates.ADD_IMAGE, post.image_insertions)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################