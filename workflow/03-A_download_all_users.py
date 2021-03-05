# -*- coding: UTF-8 -*-

"""Download and write to file the HTML for a all KiwiFarms users.

"""

###############################################################################

import os

from selenium import webdriver
import requests
from bs4 import BeautifulSoup

###############################################################################

OUTPUT_DIR = '../../data_20210224/downloaded_members'

LOGIN_URL = 'https://kiwifarms.net/login/'

URL_LIST_FILE = '../../data_20210224/member_url_list.txt'

###############################################################################

if __name__ == '__main__':

  os.makedirs( OUTPUT_DIR, exist_ok = True )

  with open( URL_LIST_FILE, 'r' ) as f:
    url_list = f.read().split('\n')

  driver = webdriver.Chrome()
  driver.get(LOGIN_URL)
  soup = BeautifulSoup( driver.page_source, 'lxml' )

  username_id = soup.find('input', {'autocomplete' : 'username'})['id']
  password_id = soup.find('input', {'type' : 'password'})['id']

  driver.find_element_by_id(username_id).send_keys(os.getenv('KIWIFARMS_USERNAME'))
  driver.find_element_by_id(password_id).send_keys(os.getenv('KIWIFARMS_PASSWORD'))
  driver.find_element_by_css_selector( '.button--primary.button.button--icon.button--icon--login' ).click( )

  for i, url in enumerate( url_list ):

    print( i, url )

    try:

      driver.get( url + '#about' )

      with open( os.path.join( OUTPUT_DIR, f'{i}.html' ), 'w' ) as f:
        f.write( driver.page_source )

    except:
      print( 'FAILED', i, url )

###############################################################################