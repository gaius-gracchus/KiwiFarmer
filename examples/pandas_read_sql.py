# -*- coding: UTF-8 -*-

"""Read column from table in database
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from kiwifarmer import base, templates

###############################################################################

COMMAND = 'SELECT post_url FROM posts'

OUTPUT_POST_URL_LIST = '../../data_fresh/post_url_list.txt'

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


  df = pd.read_sql( sql = COMMAND, con = cnx )

  df.to_csv( OUTPUT_POST_URL_LIST, sep = '\n', header = False, index = False )

  cnx.close( )



###############################################################################