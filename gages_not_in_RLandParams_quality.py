#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
import numpy as np 
from string import *
from OneDayNWMCom import *

def main(argv):
   """
     function to get input arguments
   """
   inputfile = ''
   outputfile = ''
   try:
	   opts, args = getopt.getopt(argv,"hi:o:c:p:",["id=", "od=", "com=", "pdy=" ])
   except getopt.GetoptError:
      print 'ncks.py -i <inputfile> -o <outputfile> -c <comdir> -p <pdy>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print   \
          'ncks.py -i <inputfile> -o <outputfile>' 
         sys.exit()
      elif opt in ('-i', "--id"):
         inputfile = arg
         if not os.path.exists( inputfile ):
           if not os.path.isdir( inputfile ):
             print 'input file ', inputfile, ' does not exist!'
             sys.exit()
      elif opt in ('-o', "--od" ):
         outputfile = arg
	 print 'output file: ', outputfile
      elif opt in ('-c', "--com"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print 'NWM COM dir ', comdir, ' does not exist!'
             sys.exit()
      elif opt in ('-p', "--pdy" ):
         pdy = arg
	 print 'pdy: ', pdy
  
   print 'input file is "', inputfile, '"'
   print 'output file is "', outputfile, '"'
   print 'com dir is "', comdir, '"'
   print 'pdy is "', pdy, '"'

   return (inputfile, outputfile, comdir, pdy)

def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True



if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

   infile = pgmopt[0]
   outfile = pgmopt[1]
   comdir = pgmopt[2]
   pdy = str( pgmopt[3] )

   sta_file = open( infile, "r")

   out_file = open( outfile, "w")

   com= OneDayNWMCom( comdir, pdy )
   all_time_sta_flow_qual=com.getUSGSStationRealTimeAllTimeStationStreamFlowQuality()
   for k in all_time_sta_flow_qual.keys():
      print k
   starttime = datetime.strptime( pdy + "00", "%Y%m%d%H")
   endtime = starttime + timedelta( days = 1 )
   d = timedelta( minutes = 15 )
   for line in sta_file:
        staID=line.strip( ' \t\n\r')
	print staID

	out_file.write( staID + " : " + "   time                flow           quality\n" )
	
	currenttime = starttime
	while currenttime < endtime:
#	    print currenttime
	    timekey = currenttime.strftime( "%Y-%m-%d_%H:%M:00" )
	    try: 
	        out_file.write( "               " + timekey + "  " + \
			       str( all_time_sta_flow_qual[ timekey ][staID][0] ) + \
                         "   " + str( all_time_sta_flow_qual[ timekey ][staID][1] ) + "\n" ) 
	    except KeyError:
	        out_file.write( "               " + timekey + "  " + 'Station not found!' + "\n" ) 
	    print timekey, all_time_sta_flow_qual[ timekey ].get( staID, 'Station not found!' )
	    currenttime += d
#        break;
	out_file.write( "\n" )

   sta_file.close()
   out_file.close()

