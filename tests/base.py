# -*- coding: UTF-8 -*-

"""Tests for to kiwifarms.base module.

The full set of tests for this module can be evaluated by executing the
command::

  $ python -m pytest tests/base.py

from the project root directory.

"""

###############################################################################

import os

import pytest
import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import (
  base,
  functions,
  templates, )

###############################################################################

@pytest.fixture( scope = 'module' )
def mysql_connection( ):

  """SetUp/TearDown fixture to create and delete test MySQL database for
  evaluating insertions and templates.
  """

  # create test database
  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    use_pure = False,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True  )

  cursor = cnx.cursor()
  cursor.execute(
    'CREATE DATABASE IF NOT EXISTS kiwifarms_test character set utf8mb4 collate utf8mb4_bin' )

  cnx.commit()

  cursor.close()
  cnx.close()

  # populate test database with tables based on defined templates
  #---------------------------------------------------------------------------#

  cnx = mysql.connector.connect(
    user = os.getenv( 'KIWIFARMER_USER'),
    password = os.getenv( 'KIWIFARMER_PASSWORD' ),
    host = '127.0.0.1',
    database = 'kiwifarms_test',
    use_pure = False,
    charset = 'utf8mb4',
    collation = 'utf8mb4_bin',
    use_unicode = True  )

  cursor = cnx.cursor()

  for table_name in templates.TABLES.keys( ):
    table_description = templates.TABLES[table_name]
    try:
      cursor.execute(table_description)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        pass
      else:
        print(err.msg)
    else:
      pass

  # make cursor variable available to tests
  #---------------------------------------------------------------------------#

  yield cursor

  # delete test database
  #---------------------------------------------------------------------------#

  cursor.execute( 'DROP DATABASE kiwifarms_test' )

  cnx.commit()

  cursor.close()
  cnx.close()

  return None

###############################################################################

def test_Thread( resources, mysql_connection ):

  thread = base.Thread( thread_page = resources[ 'thread_page' ] )

  thread_insertion = thread.thread_insertion

  cursor = mysql_connection

  cursor.execute(templates.ADD_THREAD, thread_insertion)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Page( resources, mysql_connection ):

  page = base.Page( thread_page = resources[ 'thread_page' ] )

  post_soups = page.get_post_soups( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Post( resources, mysql_connection ):

  post = base.Post( post = resources[ 'post' ] )

  post_insertion = post.post_insertion
  blockquote_insertions = post.blockquote_insertions
  link_insertions = post.link_insertions
  image_insertions = post.image_insertions

  cursor = mysql_connection

  cursor.execute(templates.ADD_POST, post_insertion)
  cursor.executemany(templates.ADD_BLOCKQUOTE, blockquote_insertions)
  cursor.executemany(templates.ADD_LINK, link_insertions)
  cursor.executemany(templates.ADD_IMAGE, image_insertions)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_ReactionPage( resources, mysql_connection ):

  reaction_page = base.ReactionPage( reaction_page = resources[ 'reaction_page' ] )

  reaction_list = reaction_page.get_reaction_soups( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Reaction( resources, mysql_connection ):

  reaction = base.Reaction(
    reaction = resources[ 'reaction' ], post_id = 12 )

  reaction_insertion = reaction.reaction_insertion

  cursor = mysql_connection

  cursor.execute(templates.ADD_REACTION, reaction_insertion)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_User( resources, mysql_connection ):

  user = base.User(
    user_page = resources[ 'user_page' ] )

  user_insertion = user.user_insertion

  cursor = mysql_connection

  cursor.execute(templates.ADD_USER, user_insertion)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_Following( resources, mysql_connection ):

  following = base.Following(
    following_page = resources[ 'following_page' ] )

  following_insertions = following.following_insertions

  cursor = mysql_connection

  cursor.executemany(templates.ADD_FOLLOWING, following_insertions)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def test_TrophyPage( resources, mysql_connection ):

  trophy_page = base.TrophyPage(
    user_page = resources[ 'user_about_page' ] )

  trophy_insertions = trophy_page.trophy_insertions

  cursor = mysql_connection

  cursor.executemany(templates.ADD_TROPHY, trophy_insertions)

###############################################################################