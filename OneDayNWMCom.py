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

      def getUSGSTimeSlicesNumOfStationsByCycle( self, cycle ):
          numofstations = []
          for com in self.oneDayCom:
             if com.cycle == format( cycle, ">02d" ):
               numofstations += com.getTimeSlicesNumberOfStations()
               break
          return numofstations

      def getUSACETimeSlicesNumOfStationsByCycle( self, cycle ):
          numofstations = []
          for com in self.oneDayCom:
             if com.cycle == format( cycle, ">02d" ):
               numofstations += \
                        com.getTimeSlicesNumberOfStations('ace_timeslices' )
               break
          return numofstations

      def getCanadianTimeSlicesNumOfStationsByCycle( self, cycle ):
          numofstations = []
          for com in self.oneDayCom:
             if com.cycle == format( cycle, ">02d" ):
               numofstations += \
                        com.getTimeSlicesNumberOfStations('canada_timeslices' )
               break
          return numofstations

      def getRFCTimeSlicesNumOfStationsByCycle( self, cycle ):
          numofstations = []
          for com in self.oneDayCom:
             if com.cycle == format( cycle, ">02d" ):
               numofstations += \
                        com.getTimeSlicesNumberOfStations('rfc_timeslices' )
               break
          return numofstations

      def getUSGSStationRealTimeStreamFlow( self, stationId ):
          flows = []
          for com in self.oneDayCom:
             flows += \
                  com.getUSGSStationRealTimeStreamFlow(stationId)
          return flows

      def getUSGSStationRealTimeAllTimeStationStreamFlowQuality( self, cycle=None ):
          all_time_sta_flow_qual = {} 
          print( "cycle = ", cycle )
          if cycle is not None:
            for com in self.oneDayCom:
               if com.cycle == format( cycle, ">02d" ):
                  time_sta_flow_qual = \
                      com.getUSGSStationRealTimeAllTimeStationStreamFlowQuality()
                  for k in time_sta_flow_qual.keys():
                     all_time_sta_flow_qual[ k ] = time_sta_flow_qual[ k ]
                  break
          else:
            for com in self.oneDayCom:
               time_sta_flow_qual = \
                    com.getUSGSStationRealTimeAllTimeStationStreamFlowQuality()
               for k in time_sta_flow_qual.keys():
                       all_time_sta_flow_qual[ k ] = time_sta_flow_qual[ k ]

          return all_time_sta_flow_qual

      def getForecastPoint( self,  wrfhydr_chn_pts, latlon):
              chn_pts = netCDF4.Dataset( wrfhydr_chn_pts, "r" )

              dim = chn_pts.dimensions[ "feature_id" ]
              print( dim )
              print( dim.size )

              feaidlist = []
              for id in range( 0, dim.size ):
                   feaidlist.append( ( chn_pts.variables["feature_id"][id], \
                      (chn_pts.variables["longitude"][id] - latlon[1]) * \
                      (chn_pts.variables["longitude"][id] - latlon[1]) +\
                      (chn_pts.variables["latitude"][id] - latlon[0]) * \
                      (chn_pts.variables["latitude"][id] - latlon[0]) ) )
                   print( id, chn_pts.variables["feature_id"][id], \
                           chn_pts.variables["longitude"][id] - latlon[1], \
                           chn_pts.variables["latitude"][id] - latlon[0] )

              sortedfeaid = sorted( feaidlist, key=lambda id: id[1] )

              print( "nearst feature id = ", sortedfeaid[ 0 ] )
              return sortedfeaid[ 0 ]

              chn_pts.close()

      def getStreamFlowByFeatureID( self, case, feaID, tmorf=0 ):
          flows = []
          for com in self.oneDayCom:
             flow = com.getStreamFlowByFeatureID( case, feaID, tmorf )
             if flow:
               flows.append( flow )
          return flows

      def getForecastStreamFlowByFeatureID( self, case, feaID, cycle ):
          flows = []
          for com in self.oneDayCom:
             print( com.cycle, cycle )
             if com.cycle == format( cycle, ">02d" ):
              flows = com.getForecastStreamFlowByFeatureID( case, feaID )
              break
          return flows

      def getVariable( self, case, type, cyc, var, tmorf=0):
              return self.oneDayCom[ cyc ].getVariable( case, type, var, tmorf )

      def getComCycle( self, cyc ):
              return self.oneDayCom[ cyc ]


def getForecastPointByUSGSStation( routlinknc, gsstation):
        rutlnk = netCDF4.Dataset( routlinknc, "r" )
        links = rutlnk.variables[ "link" ][:]
        gages = rutlnk.variables[ "gages" ][:]
        rutlnk.close()

        sta = '{0: >15}'.format( gsstation )
        for g, l in  zip( gages, links ):
#               print( netCDF4.chartostring(np.asarray(g)), l, sta)
               if netCDF4.chartostring( np.asarray( g ) ) == sta:
                        return l

        return None

        #gl = zip( gages, links )
#
#              gl.sort()
#
#              link_sorted = [ l for g, l in gl ]
#              gage_sorted = [ g for g, l in gl ]
#
#              idx = WRFHydroProduct.index( gage_sorted, sta )
        return link_sorted[ idx ]
