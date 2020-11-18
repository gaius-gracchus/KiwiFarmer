# -*- coding: UTF-8 -*-

"""Test initialization of the `Thread` class.
"""

###############################################################################

import os
import time

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import base, templates

###############################################################################

PAGE_DIR = '../../data/downloaded_pages'

START = 0

###############################################################################

if __name__ == '__main__':

  # create database
  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    use_pure = False,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True  )

  cursor = cnx.cursor()
  cursor.execute(
    'CREATE DATABASE kiwifarms_test character set utf8mb4 collate utf8mb4_bin' )

  cnx.commit()

  cursor.close()
  cnx.close()

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = 'kiwifarms_test',
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True )

  cursor = cnx.cursor()

  for table_name in templates.TABLES.keys( ):
    table_description = templates.TABLES[table_name]
    try:
      cursor.execute(table_description)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        pass
      else:
        print(err.msg)
    else:
      pass

  #---------------------------------------------------------------------------#

  pages = os.listdir( PAGE_DIR )[ : 100 ]

  start_time = time.time( )

  for i, page_file in enumerate( pages[ START: ] ):

    # print( i + START, page_file )

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

cursor.execute( 'DROP DATABASE kiwifarms_test' )

cnx.commit()
cursor.close()
cnx.close()

end_time = time.time( )

print( f'Elapsed time: {end_time-start_time:.4f} seconds')

###############################################################################