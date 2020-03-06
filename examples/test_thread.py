# -*- coding: UTF-8 -*-

"""Test initialization of the `Thread` class.
"""

###############################################################################

import os

import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import base, templates

###############################################################################

THREAD_URL = 'https://kiwifarms.net/threads/jonathan-yaniv-jessica-yaniv-trustednerd-trustednerd-com-jy-knows-it-jy-british-columbia.49790/'

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

  thread = base.Thread( thread_url = THREAD_URL )

  cursor.execute(templates.ADD_THREAD, thread.thread_insertion)

  page_urls = thread.get_pages( )

  for page_url in page_urls:

    page = base.Page( page_url = page_url )

    post_soups = page.get_post_soups( )

    for post_soup in post_soups:

      post = base.Post( post_soup = post_soup)

      cursor.execute(templates.ADD_POST, post.post_insertion)
      cursor.executemany(templates.ADD_BLOCKQUOTE, post.blockquote_insertions)
      cursor.executemany(templates.ADD_LINK, post.link_insertions)
      cursor.executemany(templates.ADD_IMAGE, post.image_insertions)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################