# -*- coding: UTF-8 -*-

###############################################################################

import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from kiwifarmer import base, functions

###############################################################################

THREAD_URL = 'https://kiwifarms.net/threads/satanic-vampire-neo-nazis-atomwaffen-division-siegeculture.38120/'

REACTION_URL = 'https://kiwifarms.net/posts/2924919/reactions?reaction_id=0&list_only=1&page=1'

LOGIN_URL = 'https://kiwifarms.net/login/'

USER_URL = 'https://kiwifarms.net/members/magnum-dong.9983/#about'

OUTPUT_DIR = '../tests/resources_test'

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  r = requests.get( THREAD_URL )
  thread_page = BeautifulSoup( r.content, features = "lxml" )

  r = requests.get( REACTION_URL )
  reaction_page = BeautifulSoup( r.content, features = "lxml" )

  r = requests.get( USER_URL )
  user_page = BeautifulSoup( r.content, features = "lxml" )

  creation = functions.get_thread_creation( thread_page = thread_page )

  post = thread_page.find_all('div', {'class' : "message-inner"})[ 0 ]

  message = functions.get_post_message( post = post )

  # #---------------------------------------------------------------------------#

  # driver = webdriver.Chrome()
  # driver.get(LOGIN_URL)
  # login = BeautifulSoup( driver.page_source, 'lxml' )

  # username_id = login.find('input', {'autocomplete' : 'username'})['id']
  # password_id = login.find('input', {'type' : 'password'})['id']

  # driver.find_element_by_id(username_id).send_keys(os.getenv('KIWIFARMS_USERNAME'))
  # driver.find_element_by_id(password_id).send_keys(os.getenv('KIWIFARMS_PASSWORD'))
  # driver.find_element_by_css_selector( '.button--primary.button.button--icon.button--icon--login.rippleButton' ).click( )

  # driver.get( USER_URL )
  # user_page = driver.page_source

  # driver.quit()

  #---------------------------------------------------------------------------#

  for object, name in zip(
    [ thread_page, reaction_page, user_page ],
    [ 'thread_page', 'reaction_page', 'user_page' ] ):

    with open( os.path.join( OUTPUT_DIR, name + '.html' ), 'w' ) as f:

      f.write( str( object ) )

###############################################################################