import os
import gzip
from datetime import datetime, timedelta
from string import *
from NWMCom import *


class OneDayNWMCom:

      def __init__(self, comDir, pdy ):
        self.dir = comDir 
        self.pdy = pdy 
	self.oneDayCom = []

	for cyc in range(0, 24):
	   self.oneDayCom.append( NWMCom( comDir, pdy, format(cyc, ">02") ) )

      def getUSGSTimeSlices( self ):

	  usgs_timeslices = []
          for com in self.oneDayCom:
		  usgs_timeslices += com.filenames['usgs_timeslices' ]
		  com.getTimeSlicesNumberOfStations()
          return usgs_timeslices

      def getUSGSTimeSlicesNumOfStations( self ):
	  numofstations = []
          for com in self.oneDayCom:
	     numofstations += \
		  com.getTimeSlicesNumberOfStations()
          return numofstations
