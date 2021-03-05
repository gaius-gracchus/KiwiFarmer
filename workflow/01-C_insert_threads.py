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

START = 0

DATABASE = 'kiwifarms_20210224'

###############################################################################

if __name__ == '__main__':

  # Create database (you only need to do this once)
  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    passwd = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True  )

  cursor = cnx.cursor()
  cursor.execute(
    f'CREATE DATABASE {DATABASE} character set utf8mb4 collate utf8mb4_bin' )

  cnx.commit()

  cursor.close()
  cnx.close()

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

  # Process HTML files of threads, insert fields into `threads` table
  #---------------------------------------------------------------------------#

  threads = os.listdir( THREAD_DIR )
  N_threads = len( threads )

  for i, thread_file in enumerate( threads[ START: ] ):

    print( f'[ {i + START} / {N_threads} ]', thread_file )

    with open( os.path.join( THREAD_DIR, thread_file ), 'r' ) as f:

      thread_soup = BeautifulSoup( f.read( ), 'lxml' )

    thread = base.Thread( thread_page = thread_soup )

    cursor.execute(templates.ADD_THREAD, thread.thread_insertion)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################