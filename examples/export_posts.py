# -*- coding: UTF-8 -*-

"""Create a connection to an existing MySQL database and create tables for
storing data
"""

###############################################################################

import os

import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from kiwifarmer import templates

###############################################################################

QUERY = 'SELECT * FROM posts'

###############################################################################

if __name__ == '__main__':

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    use_pure = False,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True  )

  # df = pd.read_sql( QUERY, con = cnx )

  # cnx.close()

  # df.to_csv( '../../data/posts/csv')

###############################################################################
