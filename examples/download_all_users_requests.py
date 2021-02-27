import os

import requests
from bs4 import BeautifulSoup

USERNAME = os.getenv( 'KIWIFARMS_USERNAME' )
PASSWORD = os.getenv( 'KIWIFARMS_PASSWORD' )

OUTPUT_FILE = '../../member_test.html'

with requests.Session( ) as req:

  r = req.get( "https://kiwifarms.net/login/login" )
  soup = BeautifulSoup(r.text, 'html.parser')
  token = soup.find("input", {'name': '_xfToken'}).get("value")
  data = {
    'username': USERNAME,
    'password': PASSWORD,
    'remember': '1',
    '_xfRedirect': '/',
    '_xfToken': token
  }
  r = req.post("https://kiwifarms.net/login/login", data=data)

  r = req.get( "https://kiwifarms.net/members/simon-belmont.8/")

  with open( OUTPUT_FILE, 'wb' ) as f:
    f.write( r.content )
  # print(r)