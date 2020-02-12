import re
import netCDF4     
import numpy as np 
from string import *
import bisect

def index(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
           return i
    raise ValueError

class WRFHydroModelProduct:

      def __init__(self, ncFileName ):
        self.prodId = ncFileName
        self.nc_fid = netCDF4.Dataset( ncFileName, "r" )  


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
              
      def getVariable( self, varname ):
              if varname not in self.nc_fid.variables:
                 raise RuntimeError( "Variable does not exist: " + varname )

              print( 'shape', self.nc_fid.variables[ varname ].shape )
              return self.nc_fid.variables[ varname ][:]
              
      def getVariableAttributes( self, varname, attname ):
              if varname not in self.nc_fid.variables:
                 raise RuntimeError( "Variable does not exist: " + varname )

              return self.nc_fid.variables[ varname ].getncattr( attname )
      
      def getProductType(self ):

              if re.match( r'.*\.usgsTimeSlice\.ncdf', self.prodId ) :
                      return 'usgs_timeslices'
              if re.match( r'.*\.usaceTimeSlice\.ncdf', self.prodId ) :
                      return 'ace_timeslices'
              elif re.match( r'HYDRO_RST\..*_DOMAIN1', self.prodId ) \
                or re.match( r'RESTART\..*_DOMAIN1', self.prodId )  \
                or re.match( r'nudgingLastObs\..*\.nc', self.prodId ): 
                      return 'restart'
              elif re.match( \
                      r'.*\/nwm.t[0-9]{2}z\..*\.(tm[0-9]{2}|f[0-9]{3})\.(conus|hawaii)\.nc',\
                              self.prodId ):

                      m = re.match( \
                       r'.*\/nwm.t[0-9]{2}z\.(.*)\.(.*)\.(tm[0-9]{2}|f[0-9]{3})\.(conus|hawaii)\.nc', self.prodId )
                      return m.group(2)

              else:
                      return None

      def getNumberOfStations(self, caseType ):
              if caseType != self.getProductType() :
                  raise RuntimeError( "Product is not a USGS timeslices " + \
                                  self.prodId )
              return (self.nc_fid.getncattr( 'sliceCenterTimeUTC' ), \
                               self.nc_fid.variables[ 'stationId' ].shape[0] )

      def getUSGSStationRealTimeStreamFlow(self, stationId ):
           if 'usgs_timeslices' != self.getProductType() :
             raise RuntimeError( "Product is not a USGS timeslices "+\
                                  self.prodId )
           flow = None
           for sta, dis, qual in zip( \
                   self.nc_fid.variables[ 'stationId' ],\
                   self.nc_fid.variables[ 'discharge' ], \
                   self.nc_fid.variables[ 'discharge_quality' ] ):
               station = netCDF4.chartostring( sta )
#               print(np.char.strip(station), stationId)
               if np.char.strip(station) == stationId:
                  if np.asarray( qual ) > 0:
                     flow = np.asarray( dis )
                  print ("found station: ", self.prodId, station, flow.item(0) )
                  break
#           print self.nc_fid.getncattr( 'sliceCenterTimeUTC' )
           if flow:
              return (self.nc_fid.getncattr( 'sliceCenterTimeUTC' ), \
                              flow.item(0) )
           else:
              return None

      def getUSGSStationRealTimeStreamFlowQuality(self, stationId ):
           if 'usgs_timeslices' != self.getProductType() :
             raise RuntimeError( "Product is not a USGS timeslices "+\
                                  self.prodId )
           flow = None
           dis_qual = None
           for sta, dis, qual in zip( \
                   self.nc_fid.variables[ 'stationId' ],\
                   self.nc_fid.variables[ 'discharge' ], \
                   self.nc_fid.variables[ 'discharge_quality' ] ):
               station = netCDF4.chartostring( \
                               np.asarray( sta ) ).tostring()
               if station.strip() == stationId:
                  flow = np.asarray( dis )
                  dis_qual = np.asarray( qual )
                  print ("found station: ", self.prodId, station, flow.item(0),\
                                     dis_qual.item(0) )
                  break
#           print self.nc_fid.getncattr( 'sliceCenterTimeUTC' )
           print( flow, dis_qual )
           if flow and dis_qual:
              return (self.nc_fid.getncattr( 'sliceCenterTimeUTC' ), \
                             flow.item(0), dis_qual.item(0) )
           else:
              return (self.nc_fid.getncattr( 'sliceCenterTimeUTC' ), \
                      None, None )

      def getUSGSStationRealTimeAllStationStreamFlowQuality(self ):
           if 'usgs_timeslices' != self.getProductType() :
             raise RuntimeError( "Product is not a USGS timeslices "+\
                                  self.prodId )
           sta_flow_qual = {}
           flow = None
           dis_qual = None
           for sta, dis, qual in zip( \
                   self.nc_fid.variables[ 'stationId' ],\
                   self.nc_fid.variables[ 'discharge' ], \
                   self.nc_fid.variables[ 'discharge_quality' ] ):
               station = netCDF4.chartostring( \
                               np.asarray( sta ) ).tostring().strip( ' \t\n\r')
               flow = np.asarray( dis )
               dis_qual = np.asarray( qual )

               if flow is None:
                       print( "flow is None: ", station )
               if dis_qual is None:
                       print( "dis_qual is None: ", station )
               if ( flow is not None ) and ( dis_qual is not None ):
                       sta_flow_qual[ station ] = ( flow.item(0), dis_qual.item(0) )
               else:
                       sta_flow_qual[ station ] = ( None, None )

#           print self.nc_fid.getncattr( 'sliceCenterTimeUTC' )
           return sta_flow_qual

      def getUSGSStationRealTimeCenterTime(self ):
           if 'usgs_timeslices' != self.getProductType() :
             raise RuntimeError( "Product is not a USGS timeslices "+\
                                  self.prodId )
           return self.nc_fid.getncattr( 'sliceCenterTimeUTC' )

      def getStreamFlowByFeatureID(self, feaID ):
              print( "type = ",  self.getProductType()[0:10] )
              print( "product:", self.prodId )
              if 'channel_rt' != self.getProductType()[0:10] :
                      raise RuntimeError( "Product is not a channel_rt: " + \
                                  self.prodId )
              dim = self.nc_fid.dimensions[ "feature_id" ]
              print( 'feaID = ', feaID )
              print( 'dim = ', dim )

              flow=self.nc_fid.variables[ "streamflow" ]
#              print flow
              idx = index( self.nc_fid.variables[ "feature_id" ], feaID )

              print( flow[idx] )
              return flow[idx] 

      def close(self):
         self.nc_fid.close()
