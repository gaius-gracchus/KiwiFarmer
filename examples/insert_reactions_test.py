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

REACTION_PAGE_DIR = '../../data_fresh/downloaded_reactions'

START = 0

OUTPUT_DIR = '../../data_fresh/reactions_pandas'

###############################################################################

if __name__ == '__main__':

  reactions = [ ]

  reaction_pages = sorted( os.listdir( REACTION_PAGE_DIR ) )

  for i, reaction_page_file in enumerate( reaction_pages[ START: ] ):

    print( f'{i} / {len( reaction_pages )}; {reaction_page_file}' )

    with open( os.path.join( REACTION_PAGE_DIR, reaction_page_file ), 'r' ) as f:

      page_soup = BeautifulSoup( f.read( ), 'lxml' )

    reaction_page = base.ReactionPage( soup = page_soup )

    post_id = reaction_page.post_id

    reaction_soups = reaction_page.get_reaction_soups( )

    for j, reaction_soup in enumerate( reaction_soups ):

      reaction = base.Reaction(
        reaction_soup = reaction_soup,
        post_id = post_id )

      reactions.append( reaction.reaction_insertion )

  reactions_df = pd.DataFrame( reactions )

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  reactions_df.to_pickle( os.path.join( OUTPUT_DIR, 'reactions.df' ) )

###############################################################################