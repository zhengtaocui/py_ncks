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
         if not ( casetype == 'usgs' or casetype == 'usace' ):
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
numofstationsintimeslices_m4 = []

pdy_m1 = ( dt - timedelta( hours = 1) ).strftime( "%Y%m%d" )
cycle_m1 =  ( dt - timedelta( hours = 1) ).strftime( "%H" )
pdy_m2 = ( dt - timedelta( hours = 2) ).strftime( "%Y%m%d" )
cycle_m2 =  ( dt - timedelta( hours = 2) ).strftime( "%H" )
pdy_m4 = ( dt - timedelta( hours = 4) ).strftime( "%Y%m%d" )
cycle_m4 =  ( dt - timedelta( hours = 4) ).strftime( "%H" )

com = OneDayNWMCom( comdir, pdy )
if casetype == 'usgs':
  numofstationsintimeslices = com.getUSGSTimeSlicesNumOfStationsByCycle( cycle )
elif casetype == 'usace':
  numofstationsintimeslices = \
                        com.getUSACETimeSlicesNumOfStationsByCycle( cycle )
else:
  print( 'casetype: ', casetype, ' unknown!')
  sys.exit()


com_m1 = OneDayNWMCom( comdir, pdy_m1 )
com_m2 = OneDayNWMCom( comdir, pdy_m2 )
com_m4 = OneDayNWMCom( comdir, pdy_m4 )
if casetype == 'usgs':
   numofstationsintimeslices_m1 = \
		com_m1.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m1) )
   numofstationsintimeslices_m2 = \
		com_m2.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m2) )
   numofstationsintimeslices_m4 = \
		com_m4.getUSGSTimeSlicesNumOfStationsByCycle( int(cycle_m4) )
elif casetype == 'usace':
   numofstationsintimeslices_m1 = \
		com_m1.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m1) )
   numofstationsintimeslices_m2 = \
		com_m2.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m2) )
   numofstationsintimeslices_m4 = \
		com_m4.getUSACETimeSlicesNumOfStationsByCycle( int(cycle_m4) )
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
   outf.write( '\t0\t0\t0\t0')

if numofstationsintimeslices_m2:
   for s in numofstationsintimeslices_m2:
	   outf.write('\t')
	   outf.write( str(s[1]) )
else:
   outf.write( '\t0\t0\t0\t0')

if numofstationsintimeslices_m4:
   outf.write('\t')
   outf.write( str( numofstationsintimeslices_m4[0][1]) )
else:
   outf.write( '\t0' )

outf.write('\n')

outf.close()


#cleaning up

