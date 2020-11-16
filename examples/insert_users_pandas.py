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

USER_PAGE_DIR = '../../data/users'

START = 34067

OUTPUT_DIR = '../../data/users_pandas'

###############################################################################

if __name__ == '__main__':

  users = [ ]

  user_pages = sorted( os.listdir( USER_PAGE_DIR ) )

  for i, user_page_file in enumerate( user_pages[ START: ] ):

    print( f'{i + START} / {len( user_pages )}; {user_page_file}' )

    with open( os.path.join( USER_PAGE_DIR, user_page_file ), 'r' ) as f:

      user_page = BeautifulSoup( f.read( ), 'lxml' )

    user = base.User( user_page = user_page )

    users.append( user.user_insertion )

  users_df = pd.DataFrame( users )

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  users_df.to_pickle( os.path.join( OUTPUT_DIR, 'users.df' ) )

###############################################################################