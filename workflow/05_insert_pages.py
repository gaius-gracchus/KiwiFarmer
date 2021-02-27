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

START = 91616

DATABASE = 'kiwifarms_20210224'

###############################################################################

if __name__ == '__main__':

  # Create database (you only need to do this once)
  #---------------------------------------------------------------------------#

  # cnx = mysql.connector.connect(
  #   user = os.getenv( 'KIWIFARMER_USER'),
  #   passwd = os.getenv( 'KIWIFARMER_PASSWORD' ),
  #   host = '127.0.0.1',
  #   charset = 'utf8mb4',
  #   collation = 'utf8mb4_bin',
  #   use_unicode = True  )

  # cursor = cnx.cursor()
  # cursor.execute(
  #   f'CREATE DATABASE {DATABASE} character set utf8mb4 collate utf8mb4_bin' )

  # cnx.commit()

  # cursor.close()
  # cnx.close()

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

  # for table_name in templates.TABLES.keys( ):
  #   table_description = templates.TABLES[table_name]
  #   try:
  #     print("Creating table {}: ".format(table_name), end='')
  #     cursor.execute(table_description)
  #   except mysql.connector.Error as err:
  #     if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
  #       print("already exists.")
  #     else:
  #       print(err.msg)
  #   else:
  #     print("OK")

  # Process HTML files of pages, insert fields into `post` table in database
  #---------------------------------------------------------------------------#

  pages = os.listdir( PAGE_DIR )

  for i, page_file in enumerate( pages[ START: ] ):

    print( i + START, page_file )

    with open( os.path.join( PAGE_DIR, page_file ), 'r' ) as f:

      thread_page = BeautifulSoup( f.read( ), 'lxml' )

    page = base.Page( thread_page = thread_page )

    post_soups = page.get_post_soups( )

    for j, post in enumerate( post_soups ):

      post = base.Post( post = post )

      # print( f'page: {i + START} ({page_file})\npost: {j}\nusername: {post.post_author_username}\npost_id: {post.post_id}\npost_text: {post.post_text}\n\n')
      # for k, l in enumerate( post.link_insertions ):
      #   print( k, l['link_source'])
      #   print('\n')

      cursor.execute(templates.ADD_POST, post.post_insertion)
      cursor.executemany(templates.ADD_BLOCKQUOTE, post.blockquote_insertions)
      cursor.executemany(templates.ADD_LINK, post.link_insertions)
      cursor.executemany(templates.ADD_IMAGE, post.image_insertions)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################