# -*- coding: UTF-8 -*-

"""Test initialization of the `Thread` class.
"""

###############################################################################

import os

import mysql.connector
from mysql.connector import errorcode

from kiwifarmer import base, templates

###############################################################################

THREAD_URL = 'https://kiwifarms.net/threads/omg-omg-system-shock-2-good-old-games-tomorrow.184/'

if __name__ == '__main__':

  thread = base.Thread( thread_url = THREAD_URL )

  page_urls = thread.get_pages( )

  for page_url in page_urls:

    page = base.Page( page_url = page_url )

    post_soups = page.get_post_soups( )

    for post_soup in post_soups:

      post = base.Post( post_soup = post_soup)

###############################################################################