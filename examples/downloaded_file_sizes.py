# -*- coding: UTF-8 -*-

"""Analyze downloaded file size and timestamp
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
import shutil

import matplotlib.pyplot as plt
import numpy as np

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

DOWNLOAD_DIR = '../../data_fresh/downloaded_pages/'

THRESHOLD_KB = 40 * 1024

BAD_DIR = '../../data_fresh/bad_downloaded_pages'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

files = os.listdir( DOWNLOAD_DIR )
files = [ os.path.join( DOWNLOAD_DIR, file ) for file in files ]

sizes = [ os.path.getsize( file ) for file in files ]
times = [ os.path.getmtime( file ) for file in files ]

bad_files = [ file for file in files if os.path.getsize( file ) < THRESHOLD_KB ]
print( len( bad_files ) )

[ os.remove( file ) for file in bad_files ]

files = os.listdir( DOWNLOAD_DIR )
files = [ os.path.join( DOWNLOAD_DIR, file ) for file in files ]
bad_files = [ file for file in files if os.path.getsize( file ) < THRESHOLD_KB ]
print( len( bad_files ) )

# plt.plot( times, sizes, '.' )
# plt.show( )

# plt.hist( sizes, bins = np.logspace( 0, 6, 101 ) )
# plt.xscale( 'log' )
# plt.show( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
