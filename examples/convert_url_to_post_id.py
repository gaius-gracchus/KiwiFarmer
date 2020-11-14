# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

INPUT_FILE = '../../data_fresh/thread_post_url_list'

OUTPUT_FILE = '../../data_fresh/thread_post_id_list.txt'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

with open( INPUT_FILE, 'r' ) as f:
  urls = f.read( ).split( '\n' )

ids = [ url.split( '-' )[ -1 ] for url in urls ]

with open( OUTPUT_FILE, 'w' ) as f:
  for id in ids:
    f.write( f'https://kiwifarms.net/posts/{id}/reactions?reaction_id=0&list_only=1&page=1\n' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#