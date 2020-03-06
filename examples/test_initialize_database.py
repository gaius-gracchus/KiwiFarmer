# -*- coding: UTF-8 -*-

"""Create a connection to an existing MySQL database and create tables for
storing data
"""

###############################################################################

import os

import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import templates

###############################################################################

if __name__ == '__main__':

  # cnx = mysql.connector.connect(
  #   user = os.getenv( 'KIWIFARMER_USER'),
  #   password = os.getenv( 'KIWIFARMER_PASSWORD' ),
  #   host = '127.0.0.1',
  #   use_pure = False,
  #   charset = 'utf8mb4',
  #   collation = 'utf8mb4_bin',
  #   use_unicode = True  )

  # cursor = cnx.cursor()
  # cursor.execute("CREATE DATABASE kiwifarms character set utf8mb4 collate utf8mb4_bin")

  # cnx.commit()

  # cursor.close()
  # cnx.close()

  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = 'kiwifarms',
    use_pure = False,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True  )

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

  cnx.close()

###############################################################################