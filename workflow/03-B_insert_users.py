# -*- coding: UTF-8 -*-

"""Test initialization of the `User` class.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from kiwifarmer import base, templates

###############################################################################

USER_PAGE_DIR = '../../data_20210224/downloaded_members'

START = 0

DATABASE = 'kiwifarms_20210224'

###############################################################################

if __name__ == '__main__':

  # Create tables in database (you only need to do this once)
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

  # Create tables in database (you only need to do this once)
  #---------------------------------------------------------------------------#

  cursor = cnx.cursor()

  user_pages = os.listdir( USER_PAGE_DIR )

  for i, user_page_file in enumerate( user_pages[ START: ] ):

    print( f'{i + START} / {len( user_pages )}; {user_page_file}' )

    with open( os.path.join( USER_PAGE_DIR, user_page_file ), 'r' ) as f:

      user_page = BeautifulSoup( f.read( ), 'lxml' )

    user = base.User( user_page = user_page )

    cursor.execute(templates.ADD_USER, user.user_insertion)

  cnx.commit()
  cursor.close()
  cnx.close()

###############################################################################