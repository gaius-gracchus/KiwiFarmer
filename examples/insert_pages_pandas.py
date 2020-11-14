# -*- coding: UTF-8 -*-

"""Test initialization of the `Thread` class.
"""

###############################################################################

import os

from bs4 import BeautifulSoup
import mysql.connector
from mysql.connector import errorcode
import pandas as pd

from kiwifarmer import base, templates

###############################################################################

PAGE_DIR = '../../data_fresh/downloaded_threads'

START = 0

OUTPUT_DIR = '../../data_fresh/threads_posts_pandas'

###############################################################################

if __name__ == '__main__':

  posts = [ ]
  blockquotes = [ ]
  links = [ ]
  images = [ ]

  pages = os.listdir( PAGE_DIR )

  for i, page_file in enumerate( pages[ START: ] ):

    print( f'{i} / {len( pages )}' )

    with open( os.path.join( PAGE_DIR, page_file ), 'r' ) as f:

      page_soup = BeautifulSoup( f.read( ), 'lxml' )

    page = base.Page( input = page_soup )

    post_soups = page.get_post_soups( )

    for j, post_soup in enumerate( post_soups ):

      post = base.Post( post_soup = post_soup)

      posts.append(  post.post_insertion )
      blockquotes.append( post.blockquote_insertions )
      links.append( post.link_insertions )
      images.append( post.image_insertions )

  posts_df = pd.DataFrame( posts )
  blockquotes_df = pd.DataFrame( blockquotes )
  links_df = pd.DataFrame( links )
  images_df = pd.DataFrame( images )

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  posts_df.to_pickle( os.path.join( OUTPUT_DIR, 'posts.df' ) )
  blockquotes_df.to_pickle( os.path.join( OUTPUT_DIR, 'blockquotes.df' ) )
  links_df.to_pickle( os.path.join( OUTPUT_DIR, 'links.df' ) )
  images_df.to_pickle( os.path.join( OUTPUT_DIR, 'images.df' ) )

###############################################################################