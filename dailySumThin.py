#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
import numpy as np 
import ftptools, tarfile
from string import *
from datetime import datetime
from NWMCom import NWMCom

def main(argv):
   """
     function to get input arguments
   """
   comdir = ''
   pdy = ''
   outdir = ''
   try:
	   opts, args = getopt.getopt(argv,"hd:t:o:",\
			   ["dir=", "pdy=", "outdir=" ])
   except getopt.GetoptError:
      print  \
        'checkNWMProducts.py -d <comdir> -t <pdy> -o <outdir>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print  \
	   'checkNWMProducts.py -d <comdir> -t <pdy> -o <outdir>' 
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print 'com dir ', comdir, ' does not exist!'
             sys.exit()
      elif opt in ('-t', "--pdy" ):
         pdy = arg
      elif opt in ('-o', "--outdir" ):
         outdir=arg
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (comdir, pdy, outdir)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
pdy = pgmopt[1]
outdir = pgmopt[2]

outdir = outdir + '/' + pdy

if not os.path.isdir( outdir ):
    os.makedirs( outdir )

for cyc in range( 0, 24 ):
  cycle = format( cyc, ">02")
  print "cycle = ", cycle
  nwmcom = NWMCom( comdir, pdy, cycle )

#  nwmcom.thin_fe_products( 'fe_analysis_assim', 'RAINRATE', outdir )
#  nwmcom.thin_fe_products( 'fe_short_range', 'RAINRATE', outdir )
#
#  if cyc == 6:
#    nwmcom.thin_fe_products( 'fe_medium_range', 'RAINRATE', outdir )
#
  if cyc == 0 or cyc == 6 or cyc == 12 or cyc == 18 :
    nwmcom.get_fe_long_range_daily_sum(1, outdir)
    nwmcom.get_fe_long_range_daily_sum(2, outdir)
    nwmcom.get_fe_long_range_daily_sum(3, outdir)
    nwmcom.get_fe_long_range_daily_sum(4, outdir)

#fe_long = nwmcom.getFE_Long_Range_filenames( 1 )
#print fe_long

tarfilename = 'nwm.fe_long_range_thin_daily_rainrate.' + pdy
tarfiledir = outdir[:-8] + tarfilename
os.mkdir( tarfiledir )
tar = tarfile.open(tarfiledir + '/' + tarfilename + '.tar', 'w')
tar.add( outdir, tarfilename )
tar.close()

#filelist = [ f for f in os.listdir( ourdir ) \
#		if f.endwith( "conus.nc_rainrate_dailysum.gz" ) ]
#for f in filelist:
#	os.remove( f )
shutil.rmtree( outdir )

#print "start ftp: " + str(datetime.now())
#ftptools.upload_all( "ftp.nohrsc.noaa.gov", "anonymous", "anonymous", \
#		tarfiledir, "/incoming")
#print "ftp done: " + str(datetime.now())
