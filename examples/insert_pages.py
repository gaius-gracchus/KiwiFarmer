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

PAGE_DIR = '../../data/downloaded_pages'

START = 0

###############################################################################

if __name__ == '__main__':

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = 'kiwifarms',
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True )

  cursor = cnx.cursor()

  pages = os.listdir( PAGE_DIR )

  for i, page_file in enumerate( pages[ START: ] ):

    print( i + START, page_file )

    with open( os.path.join( PAGE_DIR, page_file ), 'r' ) as f:

      page_soup = BeautifulSoup( f.read( ), 'lxml' )

    page = base.Page( input = page_soup )

    post_soups = page.get_post_soups( )

    for j, post_soup in enumerate( post_soups ):


      post = base.Post( post_soup = post_soup)

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