# -*- coding: UTF-8 -*-

"""Create list of files with all reaction pages that have at least one reaction.
"""

###############################################################################

import os

###############################################################################

INPUT_DIR='../data_20210224/downloaded_reactions'

OUTPUT_FILE_GOOD='../data_20210224/downloaded_reactions_filtered.txt'

NO_REACTIONS_STR="No one has reacted to this content yet."

###############################################################################

files = os.scandir( INPUT_DIR )

with open( OUTPUT_FILE_GOOD, 'w' ) as fout:
  for file in files:
    with open( file, 'r' ) as fin:
      doc = fin.read( )
    if NO_REACTIONS_STR not in doc:
      fout.write( file.name + '\n' )

###############################################################################