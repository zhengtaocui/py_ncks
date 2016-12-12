import netCDF4     
import numpy as np 
from string import *

class WRFHydroModelProduct:

      def __init__(self, ncFileName ):
        print ncFileName
        self.prodId = ncFileName
        self.nc_fid = netCDF4.Dataset( ncFileName, "r+" )  


      def thinToVariable(self, varname, outncfilename ):

        outnc = netCDF4.Dataset( outncfilename, "w", format=self.nc_fid.data_model )

        for name, dimension in self.nc_fid.dimensions.iteritems():
	  outnc.createDimension(name, len(dimension) \
			  if not dimension.isunlimited() else None)

	for name, variable in self.nc_fid.variables.iteritems():
	    # take out the variable you don't want
	    if name == varname or name == "time": 
              x = outnc.createVariable( name, variable.datatype, \
			    variable.dimensions)

	      for vattname in variable.ncattrs() :
	         x.setncattr( vattname, variable.getncattr( vattname ) )

              outnc.variables[name][:] = self.nc_fid.variables[name][:]

	for name in self.nc_fid.ncattrs():
	    outnc.setncattr( name,  self.nc_fid.getncattr( name ) )

        outnc.close()

      def addProduct( self, varname, other ):

         if varname not in self.nc_fid.variables or  \
			  varname not in other.nc_fid.variables:
            raise RuntimeError( "Variable does not exist: " + varname )

	 self.nc_fid.variables[ varname ][:] += \
	                          other.nc_fid.variables[ varname ][:]
	      
      def getProductType(self ):

	      if re.match( r'.*\.usgsTimeSlices\.ncdf', self.prodId ) :
		      return 'usgs_timeslices'
	      elif re.match( r'HYDRO_RST\..*_DOMAIN1\.[0-9]?', self.prodId ) \
                or re.match( r'RESTART\..*_DOMAIN1\.[0-9]?', self.prodId )  \
                or re.match( r'nudgingLastObs\..*\.nc', self.prodId ): 
		      return 'restart'
	      elif re.match( \
		      r'nwm.t[0-9]{2}z\..*\.(tm00|f[0-9]{3})\.conus\.nc',\
			      self.prodId ):

		      m = re.match( \
		       r'nwm.t[0-9]{2}z\.(.*)\..*\.conus\.nc', self.prodId )
		      return m.group(1)

              else:
		      return None

      def close(self):
         self.nc_fid.close()
