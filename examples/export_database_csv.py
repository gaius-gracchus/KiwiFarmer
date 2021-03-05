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

COMMAND = 'SELECT * FROM posts'

DATABASE = 'kiwifarms_20210224'

OUTPUT_CSV = '../../data_20210224/posts_20210224.csv'

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

  df[ 'author_user_id' ] = df[ 'author_user_id' ].astype( 'Int64' )
  df[ 'post_text' ] = df[ 'post_text' ].apply( lambda s : s.decode( 'utf-8' ) )

  df.to_csv(
    path_or_buf = OUTPUT_CSV,
    index = False,
    quoting = csv.QUOTE_NONNUMERIC )

  cnx.close( )

###############################################################################