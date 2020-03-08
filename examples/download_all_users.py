# -*- coding: UTF-8 -*-

"""Download and write to file the HTML for a all KiwiFarms users.

"""

###############################################################################

import os

from selenium import webdriver
import requests
from bs4 import BeautifulSoup

###############################################################################

OUTPUT_DIR = '../../data/users'

LOGIN_URL = 'https://kiwifarms.net/login/'
URL_FORMAT = 'https://kiwifarms.net/members/.{}/'
LAST_USER_ID = 51845

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  driver = webdriver.Chrome()
  driver.get(LOGIN_URL)
  soup = BeautifulSoup( driver.page_source, 'lxml' )

  username_id = soup.find('input', {'autocomplete' : 'username'})['id']
  password_id = soup.find('input', {'type' : 'password'})['id']

  driver.find_element_by_id(username_id).send_keys(os.getenv('KIWIFARMS_USERNAME'))
  driver.find_element_by_id(password_id).send_keys(os.getenv('KIWIFARMS_PASSWORD'))
  driver.find_element_by_css_selector( '.button--primary.button.button--icon.button--icon--login.rippleButton' ).click( )

  for i in range( 1, LAST_USER_ID + 1 ):

    try:

      driver.get( URL_FORMAT.format( i ) )

      with open( os.path.join( OUTPUT_DIR, f'{i}.html' ), 'w' ) as f:
        f.write( driver.page_source )

    except:
      pass

###############################################################################