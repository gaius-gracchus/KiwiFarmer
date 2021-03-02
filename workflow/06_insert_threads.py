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

THREAD_DIR = '../../data_20210224/downloaded_threads'

START = 19122

DATABASE = 'kiwifarms_20210224'

###############################################################################

if __name__ == '__main__':

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = DATABASE,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True )

  cursor = cnx.cursor( )

  threads = os.listdir( THREAD_DIR )

  for i, thread_file in enumerate( threads[ START: ] ):

    print( i + START, thread_file )

    with open( os.path.join( THREAD_DIR, thread_file ), 'r' ) as f:

      thread_soup = BeautifulSoup( f.read( ), 'lxml' )

    thread = base.Thread( thread_page = thread_soup )

    cursor.execute(templates.ADD_THREAD, thread.thread_insertion)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################