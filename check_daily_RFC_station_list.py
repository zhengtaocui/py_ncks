#! /usr/bin/env python
###############################################################################
#  File name: check_daily_RFC_station_list.py                                 #
#                                                                             #
#  Author     : Zhengtao Cui (Zhengtao.Cui@noaa.gov)                          #
#                                                                             #
#  Initial version date:                                                      #
#                                                                             #
#  Last modification date:  3/23/2020                                         #
#                                                                             #
#  Description: The driver to check daily rfc stations                        #
#                                                                             #
###############################################################################

import os, sys, time, urllib, getopt, re
import logging
import glob
from string import *
import operator
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, Formatter
from matplotlib.ticker import FuncFormatter
from PI_XML import PI_XML
from RFC_Forecast import RFC_Forecast
from RFCTimeSeries import RFCTimeSeries
from RFCHelper import RFCHelper
from RFC_Sites import RFC_Sites
from OneDayNWMCom import *

"""
   Get a list of RFCs who have uploaded files to NCO ftp sites.
   Author: Zhengtao Cui (Zhengtao.Cui@noaa.gov)
   Date: May 30, 2019
"""
def main(argv):
   """
     function to get input arguments
   """
   comdir = ''
   pdy = ''
   sitefile = '' 
   outputfile = ''
   try:
        opts, args = getopt.getopt(argv,"hd:p:s:o:",["dir=", "pdy=", \
                             "sites=", "output=" ])
   except getopt.GetoptError:
      print('check_daily_RFC_station_list.py -d <comdir> -p <pdy> -s <rfcsitefile> -o <outputfile>' )
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print(\
          'check_daily_RFC_station_list.py -d <comdir> -p <pdy> -s <rfcsitefile> -o <outputfile>' )
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
                 raise RuntimeError( 'FATAL Error: comdir ' + \
                                 comdir + ' does not exist!' )
      elif opt in ('-p', "--pdy" ):
         pdy = arg
      elif opt in ('-s', "--rfcsitefile" ):
         sitefile = arg
         if not os.path.exists( sitefile ):
                 raise RuntimeError( 'FATAL Error: sitefile ' + \
                                 sitefile + ' does not exist!' )
      elif opt in ('-o', "--output" ):
         outputfile=arg
  
   return (comdir, pdy, sitefile, outputfile)


t0 = time.time()

logging.basicConfig(format=\
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',\
                level=logging.INFO)
logger = logging.getLogger(__name__)
formatter = logging.Formatter(\
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#logger.setFormatter(formatter)
logger.info( "System Path: " + str( sys.path ) )

pgmopt=None

if __name__ == "__main__":
   try:
      pgmopt = main(sys.argv[1:])
   except Exception as e:
      logger.error("Failed to get program options.", exc_info=True)

comdir = pgmopt[0]
pdy = pgmopt[1]
rfcsitefile = pgmopt[2]
outputfile = pgmopt[3]

logger.info( 'com dir is "' + comdir + '"')
logger.info( 'pdy is "' + pdy + '"')
logger.info( 'RFC site file is "' + rfcsitefile + '"')
logger.info( 'output file is "' + outputfile + '"')

#
# Load ACE observed XML discharge data
#
rfcs = [ 'AB', 'SE', 'LM', 'MA', 'NE', 'WG', 'MB', 'CN', 'NW', \
             'NC', 'CB', 'OH' ]

try:
   if not os.path.isdir( comdir ):
           raise SystemExit( "FATAL ERROR: " + comdir + \
                                   " is not a directory or does not exist. ")

   rfcsites = RFC_Sites( rfcsitefile )

   com = OneDayNWMCom( comdir, pdy )

   rfc_stations = com.getEachRFCTimeSeriesUniqueStations( rfcsites )

except Exception as e:
   logger.error("Failed get RFC stations", exc_info=True)

#with open( outputfile, "w" ) as outf:
#
#  for r in rfcs:
#     outf.write( r + ' ' )
#     outf.write( str( len( rfcsites.getSitesByRFC( r + 'RFC' ) ) ) )
#     outf.write( ' ' )
#     outf.write( str( len( rfc_stations[ r ] ) ) )
#     outf.write( "\n" )

fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)

#fig.autofmt_xdate()

rfc_current_num_of_stations = []
rfc_total_possible_num_of_stations = []
for r in rfcs:
   rfc_current_num_of_stations.append( len( rfc_stations[ r ] ) )
   rfc_total_possible_num_of_stations.append( \
		   len( rfcsites.getSitesByRFC( r + 'RFC' ) ) )
y_pos = np.arange( len( rfcs ) )

ax.bar( y_pos, rfc_current_num_of_stations, color='0.75', edgecolor='k',\
		label='Actual' )
ax.bar( y_pos, list( map( operator.sub, rfc_total_possible_num_of_stations, \
		rfc_current_num_of_stations) ), 
		bottom=rfc_current_num_of_stations, color='w', edgecolor='k',\
				label='Possible' )
lgd = ax.legend()
art = [ lgd ]
for y, c, t in zip( y_pos, rfc_current_num_of_stations, \
		            rfc_total_possible_num_of_stations) :
   ax.text( y, t, str(c) + '/' + str(t), horizontalalignment='center', \
		                           verticalalignment='bottom' )

ax.set_ylim(0, 80 )
ax.set_xlabel( 'RFC Name' )
ax.set_ylabel( 'Number of Stations' )
ax.set_xticks( y_pos )
ax.set_xticklabels( rfcs )
currentdate=datetime.strptime( pdy , "%Y%m%d" )
ax.set_title( currentdate.strftime("%m/%d/%Y " ) + \
		'RFC total number of stations: ' +
	str( sum( rfc_current_num_of_stations ) ) + '/' + 
	str( sum( rfc_total_possible_num_of_stations ) ) )

canvas.print_figure(outputfile, additional_artists=art,  bbox_inches='tight')
logger.info( "Program finished in: " + \
                "{0:.1f}".format( (time.time() - t0) / 60.0 ) + \
                 " minutes" )

