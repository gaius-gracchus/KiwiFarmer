# -*- coding: UTF-8 -*-

###############################################################################

import os

import requests
from bs4 import BeautifulSoup

from kiwifarmer import base, functions

###############################################################################

THREAD_URL = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'

OUTPUT_DIR = '../tests/resources'

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  r = requests.get( THREAD_URL )
  soup = BeautifulSoup( r.content, features = "lxml" )

  creation = functions.get_thread_creation( soup = soup )

  post = soup.find_all('div', {'class' : "message-inner"})[ 0 ]

  message = functions.get_post_message( post )

  for object, name in zip(
    [ soup, creation, post, message ],
    [ 'soup', 'creation', 'post', 'message' ] ):

    with open( os.path.join( OUTPUT_DIR, name + '.html' ), 'w' ) as f:

      f.write( str( object ) )

###############################################################################