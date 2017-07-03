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
   pdy = ''
   cycle = ''
   output = ''
   try:
      opts, args = \
	      getopt.getopt(argv,"hd:p:c:o:",["dir=", "pdy=", "cycle=", "output=" ])
   except getopt.GetoptError:
      print \
        'checkCycleUSGSStatationNumbers.py -d <comdir> -p <pdy> -c <cycle> -c <output>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print  \
        'checkCycleUSGSStatationNumbers.py -d <comdir> -p <pdy> -c <cycle> -c <output>' 
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print 'com dir ', comdir, ' does not exist!'
             sys.exit()
      elif opt in ('-p', "--pdy" ):
         pdy = arg
      elif opt in ('-c', "--cycle" ):
         cycle = arg
      elif opt in ('-e', "--output" ):
         output=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (comdir, pdy, cycle, output)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
pdy = pgmopt[1]
cycle = pgmopt[2]
output = pgmopt[3]

numofstationsintimeslices = []

com = OneDayNWMCom( comdir, pdy )
numofstationsintimeslices = com.getCycleUSGSTimeSlicesNumOfStations( cycle )

print numofstationsintimeslices

#cleaning up

