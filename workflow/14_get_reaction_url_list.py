# -*- coding: UTF-8 -*-

"""Read column from table in database
"""

###############################################################################

import os
import csv

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from kiwifarmer import base, templates

###############################################################################

COMMAND = 'SELECT post_id FROM posts'

DATABASE = 'kiwifarms_20210224'

OUTPUT_CSV = '../../data_20210224/reaction_url_list.txt'

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

  df = pd.read_sql(
    sql = COMMAND,
    con = cnx )

  to_url = lambda s : f'https://kiwifarms.net/posts/{s}/reactions?reaction_id=0&list_only=1&page=1'
  url_list = df[ 'post_id' ].apply( to_url )

  url_list.to_csv( OUTPUT_CSV, header = False, index = False )

  cnx.close( )

###############################################################################