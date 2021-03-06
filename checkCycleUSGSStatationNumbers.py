#!/usr/bin/env python

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
   pdy = ''
   cycle = ''
   output = ''
   try:
      opts, args = \
                      getopt.getopt(argv,"hd:p:c:o:t:",["dir=", "pdy=", "cycle=", "output=", "casetype=" ])
   except getopt.GetoptError:
      print( \
        'checkCycleUSGSStatationNumbers.py -d <comdir> -p <pdy> -c <cycle> -o <output> -t <casetype>' )
      sys.exit(2)
   for opt, arg in opts:
      print( opt, arg )
      if opt == '-h':
         print(  \
        'checkCycleUSGSStatationNumbers.py -d <comdir> -p <pdy> -c <cycle> -o <output> -t <casetype>' )
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print( 'com dir ', comdir, ' does not exist!')
             sys.exit()
      elif opt in ('-p', "--pdy" ):
         pdy = arg
      elif opt in ('-c', "--cycle" ):
         cycle = arg
      elif opt in ('-o', "--output" ):
         output=arg
      elif opt in ('-t', "--casetype" ):
         casetype=arg
         if not ( casetype == 'usgs' or casetype == 'usace' or \
                         casetype == 'canadian' or casetype == 'rfc' ):
             print( 'casetype: ', casetype, ' unknown!')
             sys.exit()

  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (comdir, pdy, cycle, output, casetype)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
pdy = pgmopt[1]
cycle = int( pgmopt[2] )
dt = datetime.strptime( pgmopt[1] + pgmopt[2], "%Y%m%d%H" )
output = pgmopt[3]
casetype = pgmopt[4]

numofstationsintimeslices = []
numofstationsintimeslices_m1 = []
numofstationsintimeslices_m2 = []
numofstationsintimeslices_m3 = []
numofstationsintimeslices_m4 = []
numofstationsintimeslices_m6 = []
numofstationsintimeslices_m12 = []
numofstationsintimeslices_m28 = []

pdy_m1 = ( dt - timedelta( hours = 1) ).strftime( "%Y%m%d" )
cycle_m1 =  ( dt - timedelta( hours = 1) ).strftime( "%H" )
pdy_m2 = ( dt - timedelta( hours = 2) ).strftime( "%Y%m%d" )
cycle_m2 =  ( dt - timedelta( hours = 2) ).strftime( "%H" )
pdy_m3 = ( dt - timedelta( hours = 3) ).strftime( "%Y%m%d" )
cycle_m3 =  ( dt - timedelta( hours = 3) ).strftime( "%H" )
pdy_m4 = ( dt - timedelta( hours = 4) ).strftime( "%Y%m%d" )
cycle_m4 =  ( dt - timedelta( hours = 4) ).strftime( "%H" )
pdy_m6 = ( dt - timedelta( hours = 6) ).strftime( "%Y%m%d" )
cycle_m6 =  ( dt - timedelta( hours = 6) ).strftime( "%H" )
pdy_m12 = ( dt - timedelta( hours = 12) ).strftime( "%Y%m%d" )
cycle_m12 =  ( dt - timedelta( hours = 12) ).strftime( "%H" )
pdy_m28 = ( dt - timedelta( hours = 28) ).strftime( "%Y%m%d" )
cycle_m28 =  ( dt - timedelta( hours = 28) ).strftime( "%H" )

com = OneDayNWMCom( comdir, pdy )
if casetype == 'usgs':
  numofstationsintimeslices = com.getUSGSTimeSlicesNumOfStationsByCycle( cycle )
elif casetype == 'usace':
  numofstationsintimeslices = \
                        com.getUSACETimeSlicesNumOfStationsByCycle( cycle )
elif casetype == 'canadian':
  numofstationsintimeslices = \
                        com.getCanadianTimeSlicesNumOfStationsByCycle( cycle )
elif casetype == 'rfc':
  numofstationsintimeslices = \
                        com.getRFCTimeSeriesNumOfStationsByCycle( cycle )
else:
  print( 'casetype: ', casetype, ' unknown!')
  sys.exit()


com_m1 = OneDayNWMCom( comdir, pdy_m1 )
com_m2 = OneDayNWMCom( comdir, pdy_m2 )
com_m3 = OneDayNWMCom( comdir, pdy_m3 )
com_m4 = OneDayNWMCom( comdir, pdy_m4 )
com_m6 = OneDayNWMCom( comdir, pdy_m6 )
com_m12 = OneDayNWMCom( comdir, pdy_m12 )
com_m28 = OneDayNWMCom( comdir, pdy_m28 )
if casetype == 'usgs':
   numofstationsintimeslices_m1 = \
		com_m1.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m1) )
   numofstationsintimeslices_m2 = \
		com_m2.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m2) )
   numofstationsintimeslices_m3 = \
		com_m3.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m3) )
   numofstationsintimeslices_m4 = \
		com_m4.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m4) )
   numofstationsintimeslices_m6 = \
		com_m6.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m6) )
   numofstationsintimeslices_m12 = \
		com_m12.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m12) )
   numofstationsintimeslices_m28 = \
		com_m28.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m28) )
elif casetype == 'usace':
   numofstationsintimeslices_m1 = \
		com_m1.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m1) )
   numofstationsintimeslices_m2 = \
		com_m2.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m2) )
   numofstationsintimeslices_m3 = \
		com_m3.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m3) )
   numofstationsintimeslices_m4 = \
		com_m4.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m4) )
   numofstationsintimeslices_m6 = \
		com_m6.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m6) )
   numofstationsintimeslices_m12 = \
		com_m12.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m12) )
   numofstationsintimeslices_m28 = \
		com_m28.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m28) )
elif casetype == 'canadian':
   numofstationsintimeslices_m1 = \
		com_m1.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m1) )
   numofstationsintimeslices_m2 = \
		com_m2.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m2) )
   numofstationsintimeslices_m3 = \
		com_m3.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m3) )
   numofstationsintimeslices_m4 = \
		com_m4.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m4) )
   numofstationsintimeslices_m6 = \
		com_m6.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m6) )
   numofstationsintimeslices_m12 = \
		com_m12.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m12) )
   numofstationsintimeslices_m28 = \
		com_m28.getCanadianTimeSlicesNumOfStationsByCycle( int(cycle_m28) )
elif casetype == 'rfc':
   numofstationsintimeslices_m1 = \
		com_m1.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m1) )
   numofstationsintimeslices_m2 = \
		com_m2.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m2) )
   numofstationsintimeslices_m3 = \
		com_m3.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m3) )
   numofstationsintimeslices_m4 = \
		com_m4.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m4) )
   numofstationsintimeslices_m6 = \
		com_m6.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m6) )
   numofstationsintimeslices_m12 = \
		com_m12.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m12) )
   numofstationsintimeslices_m28 = \
		com_m28.getRFCTimeSeriesNumOfStationsByCycle( int(cycle_m28) )
else:
  print( 'casetype: ', casetype, ' unknown!')
  sys.exit()

print( output )
print( len( numofstationsintimeslices ) )
outf = open( output, "a+")
if numofstationsintimeslices:
   print( numofstationsintimeslices[0][0] )
   outf.write( numofstationsintimeslices[0][0] )
   outf.write('\t')
   outf.write( str( numofstationsintimeslices[0][1] ) )
else:
   outf.write( pdy[:4]+'-'+ pdy[4:6] +'-'+pdy[6:8] \
		   +'_' + format( cycle, ">02d" ) + ':00:00\t0')

if numofstationsintimeslices_m1:
   for s in numofstationsintimeslices_m1:
	   outf.write('\t')
	   outf.write( str(s[1]) )
else:
   if casetype == 'rfc':
      outf.write( '\t0')
   else:
      outf.write( '\t0\t0\t0\t0')

if numofstationsintimeslices_m2:
   for s in numofstationsintimeslices_m2:
	   outf.write('\t')
	   outf.write( str(s[1]) )
else:
   if casetype == 'rfc':
      outf.write( '\t0')
   else:
      outf.write( '\t0\t0\t0\t0')

if numofstationsintimeslices_m3:
   outf.write('\t')
   outf.write( str( numofstationsintimeslices_m3[0][1]) )
else:
   outf.write( '\t0' )

if numofstationsintimeslices_m4:
   outf.write('\t')
   outf.write( str( numofstationsintimeslices_m4[0][1]) )
else:
   outf.write( '\t0' )

if numofstationsintimeslices_m6:
   outf.write('\t')
   outf.write( str( numofstationsintimeslices_m6[0][1]) )
else:
   outf.write( '\t0' )

if numofstationsintimeslices_m12:
   outf.write('\t')
   outf.write( str( numofstationsintimeslices_m12[0][1]) )
else:
   outf.write( '\t0' )

if numofstationsintimeslices_m28:
   outf.write('\t')
   outf.write( str( numofstationsintimeslices_m28[0][1]) )
else:
   outf.write( '\t0' )

outf.write('\n')

outf.close()


#cleaning up

