import os

import requests
from bs4 import BeautifulSoup

# login url for forum, and fake forum credentials (they're real in my script)
LOGIN_URL = 'https://kiwifarms.net/login/'
KIWIFARMS_USERNAME = os.getenv( 'KIWIFARMS_USERNAME' )
KIWIFARMS_PASSWORD = os.getenv( 'KIWIFARMS_PASSWORD' )

with requests.Session() as req:
  r = req.get("https://kiwifarms.net/login/login")
  soup = BeautifulSoup(r.text, 'lxml')
  token = soup.find("input", {'name': '_xfToken'}).get("value")
  data = {
    'username': KIWIFARMS_USERNAME,
    'password': KIWIFARMS_PASSWORD,
    'remember': '1',
    '_xfRedirect': '/',
    '_xfToken': token }
  r = req.post("https://kiwifarms.net/login/login", data=data)

  user_url = 'https://kiwifarms.net/members/magnum-dong.9983/'

  r = req.get( user_url )
  print( r )
