#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
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
   comdir = ''
   startday = ''
   endday = ''
   try:
      opts, args = \
	 getopt.getopt(argv,"hd:s:e:",["dir=", "startday=", "endday=" ])
   except getopt.GetoptError:
      print \
        'checkUSGSStatationNumbers.py -d <comdir> -s <startpdy> -e <endpdy>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print  \
           'checkUSGSStatationNumbers.py -d <comdir> -s <startpdy> -e <endpdy>' 
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print 'com dir ', comdir, ' does not exist!'
             sys.exit()
      elif opt in ('-s', "--startpdy" ):
         startday = arg
      elif opt in ('-e', "--endday" ):
         endday=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (comdir, startday, endday)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
startpdy = datetime.strptime( pgmopt[1], "%Y%m%d" )
endpdy = datetime.strptime( pgmopt[2], "%Y%m%d" )

timeslices = []
oneday = timedelta( days = 1)

numofstationsintimeslices = []

dateiter = startpdy
while dateiter < endpdy:

    com = OneDayNWMCom( comdir, dateiter.strftime(  "%Y%m%d" ) )
    numofstationsintimeslices += com.getUSGSTimeSlicesNumOfStations()

    dateiter += oneday

station_date = []
station_num = []

for station in numofstationsintimeslices:
   station_num.append( station[1] )
   station_date.append( datetime.strptime( station[0], "%Y-%m-%d_%H:%M:%S" ) )

fig = Figure()
canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)
numofstationsplot, = ax.plot( station_date, station_num, linestyle='-', \
		marker='o', markersize=3, markerfacecolor='None', color='k' )

ax.xaxis.set_major_locator( mdates.DayLocator() )
ax.xaxis.set_minor_locator( mdates.HourLocator() )

ax.set_xlim( startpdy, endpdy )
fig.autofmt_xdate()

ax.grid( True )
ax.xaxis.set_major_formatter( mdates.DateFormatter('%b %d' ))

ax.set_xlabel( 'Time' )
ax.set_ylabel( 'Number of USGS Stations' )

canvas.print_figure('NumberOfUSGSStations.pdf')

#cleaning up

