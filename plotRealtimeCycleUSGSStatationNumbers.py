#!/usr/bin/env python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
#import netCDF4     
import numpy as np 
from string import *
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, Formatter
from matplotlib.ticker import FuncFormatter
#from cycler import cycler

from OneDayNWMCom import *

def main(argv):
   """
     function to get input arguments
   """
   input = ''
   output = ''
   title = ''
   try:
      opts, args = \
	      getopt.getopt(argv,"hi:o:t:",["input=", "output=", "title="])
   except getopt.GetoptError:
      print \
        'heckUSGSStatationNumbers.py -d <comdir> -s <startpdy> -e <endpdy>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print  \
           'checkUSGSStatationNumbers.py -d <comdir> -s <startpdy> -e <endpdy>' 
         sys.exit()
      elif opt in ('-i', "--input"):
         input = arg
         if not os.path.exists( input ):
           if os.path.isdir( input ):
             print 'input ', input, ' does not exist!'
             sys.exit()
      elif opt in ('-o', "--output" ):
         output = arg
      elif opt in ('-t', "--title" ):
         title=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (input, output, title)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

input = pgmopt[0]
output = pgmopt[1]
title = pgmopt[2]

station_date = []
station_num = []

for i in range(0, 10):
	station_num.append( [] )

infile = open( input, 'r' )

for line in infile:
   values = line.split()
   for i in range( 0, 10 ): 
      try:
              station_num[ i ].append( int( values[ i + 1 ] ) )
      except:
	      print "Error: ", line
	      station_num[ i ].append( 0 )
   station_date.append( datetime.strptime( values[0], "%Y-%m-%d_%H:%M:%S" ) )


legd_labels = [ '-00 min.', '-60 min.', '-45 min.', '-30 min.', '-15 min.', \
		'-120 min.', '-105 min', '-90 min,', '-75 min', '-240 min' ]

linestyles = [ '-', '--', ':', '-.']
markers = ['o','^',',', '.', 'x' ]
## Create cycler object. Use any styling from above you please
#monochrome = (cycler('color', ['k']) * cycler('linestyle',\
#              ['-', '--', ':', '=.']) * cycler('marker', ['o','^',',', '.']))
 
fig = Figure()
canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)
#ax.set_prop_cycle(monochrome)
ax.xaxis.set_major_formatter( mdates.DateFormatter('%b %d' ))
ax.xaxis.set_minor_formatter( mdates.DateFormatter('%Hz' ))

#fig.autofmt_xdate()

for i in [0, 4, 3, 2, 1, 8, 7, 6, 5, 9]:
      print i
      numofstationsplot, = ax.plot_date( station_date, station_num[i], \
	      linestyle=linestyles[ i % 4 ], label=legd_labels[ i ], \
            marker=markers[ i % 5 ], markersize=5, markerfacecolor='None', color='k' )

#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

ax.xaxis.set_major_locator( mdates.DayLocator() )
ax.xaxis.set_minor_locator( mdates.HourLocator( interval=2) )

ax.tick_params(axis='x', rotation=90)

#ax.yaxis.set_major_locator( MultipleLocator(20) )

ax.set_xlim( station_date[0] - timedelta( hours=1), \
		station_date[-1] + timedelta( hours = 1 ) )

#ax.set_ylim(0, 1000)


ax.grid( True, "minor", "x" )
ax.grid( True, "major", "y" )

ax.set_xlabel( 'Cycle' )
ax.set_ylabel( 'Number of USGS Stations' )
ax.set_title( title )
lgd = ax.legend( bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0. ) 
#ax.legend(loc='center', ncol=3, bbox_to_anchor=(0.5,-0.23))
#ax.legend( loc=2 ) 
art=[ lgd ]

canvas.print_figure(output, additional_artists=art, bbox_inches='tight')

#cleaning up

