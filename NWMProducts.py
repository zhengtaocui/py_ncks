import netCDF4     
import numpy as np 
from string import *
import WRFHydroProduct


class NWMProducts:

      def __init__(self, ncFileNames, simulType, pdy, cycle ):
        self.simulType = simulType 
        self.pdy = cycle 
        self.ncFileNames = ncFileNames
        self.prods = []
        for f in self.ncFileNames:
	    self.prods.append ( WRFHydroModelProduct( f ) )

      def isEmpty( self ):
          return not self.prods

      def getAllForecasts( self, forecastType )
           pass 
