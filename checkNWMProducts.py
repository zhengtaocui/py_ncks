#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
import numpy as np 
from string import *
from NWMCom import NWMCom

def main(argv):
   """
     function to get input arguments
   """
   comdir = ''
   pdy = ''
   cycle = ''
   try:
	   opts, args = getopt.getopt(argv,"hd:t:c:",["dir=", "pdy=", "cyc=" ])
   except getopt.GetoptError:
      print 'checkNWMProducts.py -d <comdir> -t <pdy> -c <cycle>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print 'checkNWMProducts.py -d <comdir> -t <pdy> -c <cycle>' 
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print 'com dir ', comdir, ' does not exist!'
             sys.exit()
      elif opt in ('-t', "--pdy" ):
         pdy = arg
      elif opt in ('-c', "--cyc" ):
         cycle=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (comdir, pdy, cycle)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
pdy = pgmopt[1]
cycle = pgmopt[2]

nwmcom = NWMCom( comdir, pdy, cycle )

nwmcom.checkProducts( 'short_range')
nwmcom.checkProducts( 'analysis_assim')
nwmcom.checkProducts( 'usgs_timeslices')
nwmcom.checkProducts( 'fe_short_range')
nwmcom.checkProducts( 'fe_analysis_assim')
nwmcom.checkProducts( 'restart')

if cycle == '06':
   nwmcom.checkProducts( 'medium_range')
   nwmcom.checkProducts( 'long_range_mem1')
   nwmcom.checkProducts( 'long_range_mem2')
   nwmcom.checkProducts( 'long_range_mem3')
   nwmcom.checkProducts( 'long_range_mem4')
   nwmcom.checkProducts( 'fe_medium_range')
   nwmcom.checkProducts( 'fe_long_range_mem1')
   nwmcom.checkProducts( 'fe_long_range_mem2')
   nwmcom.checkProducts( 'fe_long_range_mem3')
   nwmcom.checkProducts( 'fe_long_range_mem4')

if cycle == '00' or cycle == '12' or cycle == 18:
   nwmcom.checkProducts( 'long_range_mem1')
   nwmcom.checkProducts( 'long_range_mem2')
   nwmcom.checkProducts( 'long_range_mem3')
   nwmcom.checkProducts( 'long_range_mem4')
   nwmcom.checkProducts( 'fe_long_range_mem1')
   nwmcom.checkProducts( 'fe_long_range_mem2')
   nwmcom.checkProducts( 'fe_long_range_mem3')
   nwmcom.checkProducts( 'fe_long_range_mem4')
#cleaning up

