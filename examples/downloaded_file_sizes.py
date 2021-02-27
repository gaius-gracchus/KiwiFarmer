# -*- coding: UTF-8 -*-

"""Analyze downloaded file size and timestamp
"""

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

import os
import shutil

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import Normalize
from scipy.interpolate import interpn

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

DOWNLOAD_DIR = '../../data_fresh/downloaded_pages/'

THRESHOLD_KB = 40 * 1024

BAD_DIR = '../../data_fresh/bad_downloaded_pages'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def density_scatter( x , y, ax = None, sort = True, bins = 20, **kwargs ):

  """Scatter plot colored by 2d histogram
  """
  if ax is None :
    fig , ax = plt.subplots()
  data , x_e, y_e = np.histogram2d( x, y, bins = bins, density = True )
  z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False)

  #To be sure to plot all data
  z[np.where(np.isnan(z))] = 0.0

  # Sort the points by density, so that the densest points are plotted last
  if sort :
    idx = z.argsort()
    x, y, z = x[idx], y[idx], z[idx]

  ax.scatter( x, y, c=z, **kwargs )

  norm = Normalize(vmin = np.min(z), vmax = np.max(z))
  cbar = fig.colorbar(cm.ScalarMappable(norm = norm), ax=ax)
  cbar.ax.set_ylabel('Density')

  return ax

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

files = os.listdir( DOWNLOAD_DIR )
files = [ os.path.join( DOWNLOAD_DIR, file ) for file in files ]

# sizes = [ os.path.getsize( file ) for file in files ]
times = sorted( [ os.path.getmtime( file ) for file in files ] )

# bad_files = [ file for file in files if os.path.getsize( file ) < THRESHOLD_KB ]
# print( len( bad_files ) )

# [ os.remove( file ) for file in bad_files ]

# files = os.listdir( DOWNLOAD_DIR )
# files = [ os.path.join( DOWNLOAD_DIR, file ) for file in files ]
# bad_files = [ file for file in files if os.path.getsize( file ) < THRESHOLD_KB ]
# print( len( bad_files ) )

x = times[ :-1 ]
y = np.diff( times )

h = np.histogram2d(
  x = x,
  y = y,
  range = [ [ np.min( x ), np.max( x ) ], [ 0, 10 ] ],
  bins = [ 80, 80 ] )
plt.matshow( h[ 0 ].T, origin = 'lower'  )
plt.show()

# ax.scatter(x, y, c=z, s=100, edgecolor='')
# plt.ylim( 0, 10 )
# plt.show( )
# density_scatter( x, y, bins = [30,30] )

# plt.hist( sizes, bins = np.logspace( 0, 6, 101 ) )
# plt.xscale( 'log' )
# plt.show( )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
