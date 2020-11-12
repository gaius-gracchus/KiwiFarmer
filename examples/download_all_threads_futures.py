# -*- coding: UTF-8 -*-

"""https://stackoverflow.com/a/46144596/13026442
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
import concurrent.futures
import time

import requests
import pandas as pd

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

URL_LIST_FILE = '../../data_fresh/url_list.txt'

OUTPUT_DIR = '../../data_fresh/downloaded_threads_50'

CONNECTIONS = 50
TIMEOUT = 5

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def load_url(url, timeout):
  ans = requests.head(url, timeout=timeout)
  return ans.status_code

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

os.makedirs( OUTPUT_DIR, exist_ok = True )

with open( URL_LIST_FILE, 'r' ) as f:
  urls = f.read().split('\n')

out = [ ]

with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
  future_to_url = (executor.submit(load_url, url, TIMEOUT) for url in urls)
  time1 = time.time()
  for future in concurrent.futures.as_completed(future_to_url):
    try:
      data = future.result()
    except Exception as exc:
      data = str(type(exc))
    finally:
      # filename = os.path.join( OUTPUT_DIR, url[ 30 : -1 ].replace('/', '_') + '.html' )
      # with open( filename, 'w' ) as f:
      #   f.write( data )
      # out.append(data)

      print( data )

      # print(str(len(out)),end="\r")

  time2 = time.time()

print(f'Took {time2-time1:.2f} s')
print(pd.Series(out).value_counts())

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#