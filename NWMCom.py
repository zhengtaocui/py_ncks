import os
import re
import gzip
import glob
from datetime import datetime, timedelta
from string import *
from WRFHydroProduct import *


class NWMCom:

      def __init__(self, comDir, pdy, cycle ):
        self.dir = comDir 
        self.pdy = pdy 
        self.cycle = cycle
        self.filenames = dict( [ ('short_range', [] ), \
                                 ('short_range_hawaii', [] ),\
                                 ('medium_range_mem1', [] ),\
                                 ('medium_range_mem2', [] ),\
                                 ('medium_range_mem3', [] ),\
                                 ('medium_range_mem4', [] ),\
                                 ('medium_range_mem5', [] ),\
                                 ('medium_range_mem6', [] ),\
                                 ('medium_range_mem7', [] ),\
                                 ('long_range_mem1', []), \
                                 ('long_range_mem2', []), \
                                 ('long_range_mem3', []), \
                                 ('long_range_mem4', []), \
                                 ('analysis_assim', []), \
                                 ('analysis_assim_long', []), \
                                 ('analysis_assim_extend', []), \
                                 ('analysis_assim_hawaii', []), \
                                 ('forcing_short_range', [] ), \
                                 ('forcing_medium_range', [] ),\
                                 ('forcing_long_range_mem1', []), \
                                 ('forcing_long_range_mem2', []), \
                                 ('forcing_long_range_mem3', []), \
                                 ('forcing_long_range_mem4', []), \
                                 ('forcing_long_range_mem1_thin', []), \
                                 ('forcing_long_range_mem2_thin', []), \
                                 ('forcing_long_range_mem3_thin', []), \
                                 ('forcing_long_range_mem4_thin', []), \
                                 ('forcing_analysis_assim', []), \
                                 ('forcing_analysis_assim_extend', []), \
                                 ('forcing_analysis_assim_hawaii', []), \
                                 ('forcing_short_range_hawaii', []), \
                                 ('restart', []),            \
                                 ('restart_extend', []),            \
                                 ('restart_hawaii', []),            \
                                 ('restart_long', []),            \
                                 ('usace_timeslices', []),            \
                                 ('canada_timeslices', []),            \
                                 ('rfc_timeseries', []),            \
                                 ('usgs_timeslices', []) ] )

        for k in self.filenames.keys():
           self.getProductFilenames( k )

      def getProductFilenames( self, caseType ):

              dataTypes = [ 'terrain_rt', 'reservoir', 'land', 'channel_rt' ]
              if caseType == "short_range":
                  for datatype in dataTypes:
                     for i in range(1, 18):
                       self.filenames['short_range'].append('nwm.t' + \
                            self.cycle + 'z.short_range.' +\
                            datatype + '.f' + format( i, ">03") +     \
                            '.conus.nc' )
              elif caseType == "short_range_hawaii":
                  for datatype in dataTypes:
                     for i in range(1, 60):
                       self.filenames['short_range'].append('nwm.t' + \
                            self.cycle + 'z.short_range.' +\
                            datatype + '.f' + format( i, ">03") +     \
                            '.hawaii.nc' )
              elif caseType == "medium_range_mem1" or \
                   caseType == "medium_range_mem2" or \
                   caseType == "medium_range_mem3" or \
                   caseType == "medium_range_mem4" or \
                   caseType == "medium_range_mem5" or \
                   caseType == "medium_range_mem6" or \
                   caseType == "medium_range_mem7" :
                  for datatype in dataTypes:
                     for i in range(3, 243, 3):
                       self.filenames[caseType].append('nwm.t' + \
                            self.cycle + 'z.medium_range.' +\
                            datatype +  '_' + caseType[16:] + \
                            '.f' + format( i, ">03") +     \
                            '.conus.nc' )

              elif caseType == "analysis_assim":
                  for datatype in dataTypes:
                     for i in range(0, 3):
                        self.filenames['analysis_assim'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim.' +\
                            datatype + '.tm' + format( i, ">02" ) + \
                            '.conus.nc' )

              elif caseType == "analysis_assim_extend":
                  for datatype in dataTypes:
                     for i in range(0, 28):
                        self.filenames['analysis_assim_extend'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim_extend.' +\
                            datatype + '.tm' + format( i, ">02" ) + \
                            '.conus.nc' )

              elif caseType == "analysis_assim_long":
                  for datatype in dataTypes:
                     for i in range(0, 12):
                        self.filenames['analysis_assim_long'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim_long.' +\
                            datatype + '.tm' + format( i, ">02" ) + \
                            '.conus.nc' )

              elif caseType == "analysis_assim_hawaii":
                  for datatype in dataTypes:
                     for i in range(0, 3):
                        self.filenames['analysis_assim_extend'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim.' +\
                            datatype + '.tm' + format( i, ">02" ) + \
                            '.hawaii.nc' )

              elif caseType == "long_range_mem1" or \
                    caseType == "long_range_mem2" or \
                    caseType == "long_range_mem3" or \
                   caseType == "long_range_mem4" :

                  for datatype in [ 'reservoir', 'channel_rt' ]:
                     for i in range(6, 726, 6):
                       self.filenames[ caseType ].append('nwm.t' + \
                            self.cycle + 'z.long_range.' +\
                            datatype + '_' + caseType[14:] + \
                            '.f' + format( i, ">03") + '.conus.nc' )

                  for i in range(24, 744, 24):
                       self.filenames[ caseType ].append('nwm.t' + \
                            self.cycle + 'z.long_range.' +\
                            'land_' + caseType[14:] + \
                            '.f' + format( i, ">03") + '.conus.nc' )

              elif caseType == "forcing_analysis_assim":
                     for i in range(0, 3):
                        self.filenames['forcing_analysis_assim'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim.forcing.tm' + \
                            format( i, ">02" ) + '.conus.nc' )

              elif caseType == "forcing_analysis_assim_extend":
                     for i in range(0, 28):
                        self.filenames['forcing_analysis_assim_extend'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim_extend.forcing.tm' + \
                            format( i, ">02" ) + '.conus.nc' )

              elif caseType == "forcing_analysis_assim_hawaii":
                     for i in range(0, 3):
                        self.filenames['forcing_analysis_assim_hawaii'].append('nwm.t' + \
                            self.cycle + 'z.analysis_assim.forcing.tm' + \
                            format( i, ">02" ) + '.hawaii.nc' )

              elif caseType == "forcing_short_range_hawaii":
                     for i in range(0, 61):
                        self.filenames['forcing_short_range_hawaii'].append('nwm.t' + \
                            self.cycle + 'z.short_range.forcing.tm' + \
                            format( i, ">02" ) + '.hawaii.nc' )

              elif caseType == "forcing_short_range":
                  for i in range(1, 18):
                       self.filenames['forcing_short_range'].append('nwm.t' + \
                            self.cycle + 'z.short_range.forcing.f' +\
                            format( i, ">03") +     \
                            '.conus.nc' )

              elif caseType == "forcing_medium_range":
                  for i in range(3, 243, 3):
                       self.filenames['forcing_medium_range'].append('nwm.t' + \
                            self.cycle + 'z.medium_range.forcing.f' +\
                            format( i, ">03") +     \
                            '.conus.nc' )

              elif caseType == "forcing_long_range_mem1" or \
                    caseType == "forcing_long_range_mem2" or \
                    caseType == "forcing_long_range_mem3" or \
                   caseType == "forcing_long_range_mem4" :

                   for i in range(3, 723, 3):
                       self.filenames[ caseType ].append('nwm.t' + \
                            self.cycle + 'z.long_range' +\
                            '_' + caseType[22:] + \
                            '.forcing.f' + format( i, ">03") + '.conus.nc' )

              elif caseType == "forcing_long_range_mem1_thin" or \
                    caseType == "forcing_long_range_mem2_thin" or \
                    caseType == "forcing_long_range_mem3_thin" or \
                   caseType == "forcing_long_range_mem4_thin" :

                   for i in range(3, 723, 3):
                       self.filenames[ caseType ].append('nwm.t' + \
                            self.cycle + 'z.long_range_thin_' +\
                            caseType[22:23] + \
                            '.forcing.f' + format( i, ">03") + '.conus.nc' )

              elif caseType == "usace_timeslices" :
                 dt = \
                  datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 for i in range(0, 4 ):
                    d = timedelta( minutes = i * 15 )
                    self.filenames['usace_timeslices'].append(
                     ( dt +  d ).strftime( "%Y-%m-%d_%H:%M:00." ) + \
                     '15min.usaceTimeSlice.ncdf' )

              elif caseType == "canada_timeslices" :
                 dt = \
                  datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 for i in range(0, 4 ):
                    d = timedelta( minutes = i * 15 )
                    self.filenames['canada_timeslices'].append(
                     ( dt +  d ).strftime( "%Y-%m-%d_%H_%M_00." ) + \
                     '15min.wscTimeSlice.ncdf' )

              elif caseType == "rfc_timeseries" :
                 dt = \
                  datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 self.filenames['rfc_timeseries'].append(
                     ( dt ).strftime( "%Y-%m-%d_%H." ) + \
                     '60min.?????.RFCTimeSeries.ncdf' )

              elif caseType == "usgs_timeslices" :
                 dt = \
                  datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 for i in range(0, 4 ):
                    d = timedelta( minutes = i * 15 )
                    self.filenames['usgs_timeslices'].append(
                     ( dt +  d ).strftime( "%Y-%m-%d_%H:%M:00." ) + \
                     '15min.usgsTimeSlice.ncdf' )

              elif caseType == "restart" or \
                   caseType == "restart_extend" or \
                   caseType == "restart_long" or \
                   caseType == "restart_hawaii" :
                 dt = datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 self.filenames[ caseType ].append( 'nwm.rst.' + \
                                     self.cycle + '/RESTART.' + \
                           self.pdy + self.cycle + '_DOMAIN1')

                 self.filenames[ caseType ].append( 'nwm.rst.' +   \
                                     self.cycle + '/HYDRO_RST.' +       \
                                     dt.strftime( "%Y-%m-%d_%H:00" ) \
                           + '_DOMAIN1' )

                 self.filenames[ caseType ].append( 'nwm.rst.' +   \
                                self.cycle +                        \
                                '/nudgingLastObs.' +                \
                                dt.strftime( "%Y-%m-%d_%H:%M:00" )  \
                                + '.nc' )

              else:
                      raise RuntimeError( "FATAL ERROR: Unknown caseType: " \
                        + caseType )

#      def getFE_Long_Range_filenames( self, mem ):
#            if mem < 5 and mem > 0 :
#              return self.filenames[ 'fe_long_range_mem' + str( mem ) ]

      def unzip( self, file, outdir ):
            if file.endswith( '.gz' ):
                unzippedfile = outdir + '/' + os.path.basename( file )[:-3]
                inF = gzip.open( file, 'rb' )
                outF = open( unzippedfile, 'wb' )
                file_content = inF.read()
                inF.close()
                outF.write( file_content )
                outF.close()
                return unzippedfile
            else:
                return file
            
      def zip( self, file ):
           inF = open(  file, 'rb' )
           outF = gzip.open( file +'.gz', 'wb' )
           outF.writelines( inF )
           outF.close()
           os.remove( file )

      def get_fe_long_range_daily_sum( self, mem, outdir ):
            if mem < 5 and mem > 0 :
               # find the 12z files
               startseq = ( ( 24 + ( 12 - int( self.cycle ) ) ) % 24 ) / 3
               endseq = 240 - ( 8 - startseq )
               for i in range(startseq, endseq, 8):
                  file = self.dir + '/nwm.' + self.pdy + \
                           '/forcing_long_range_mem' + str( mem ) + '/' + \
                    self.filenames[ \
                         'forcing_long_range_mem' + str( mem ) + '_thin' ][ i ]

                  file = self.unzip( file, outdir ) 

                  prod = WRFHydroModelProduct( file )

                  for j in range(1, 8 ):
                     f = self.dir + '/nwm.' + self.pdy + \
                         '/forcing_long_range_mem' + str( mem ) + '/' + \
                           self.filenames[ \
                         'forcing_long_range_mem' + str( mem ) + '_thin' ][i+j]

                     f = self.unzip( f, outdir ) 

                     p = WRFHydroModelProduct( f )

                     prod.addProduct( "RAINRATE", p )
                     p.close()
                     os.remove( f )

                  prod.thinToVariable( "RAINRATE", file+'_rainrate_dailysum')
                  prod.close()
                  os.remove( file )
                  self.zip( file+'_rainrate_dailysum' )
                  print( file +'_rainrate' )

      def thin_fe_products( self, caseType, thinvariable, outdir ): 
              for f in self.filenames[caseType]:
                  fn = self.dir + '/nwm.' + self.pdy + \
                                   '/' +caseType + '/' + f
                  outfn = self.unzip( fn, outdir )
                  prod = WRFHydroModelProduct( outfn )
                  print( outfn )
                  print( outfn[:-3] + '.thinned.nc' )
                  prod.thinToVariable( thinvariable, outfn[:-3] + \
                                                        '.thinned.nc' )
                  prod.close()
                  os.remove( outfn )
                  self.zip( outfn[:-3] + '.thinned.nc' )

      def missingProducts( self, caseType ): 
              missing = []
              for f in self.filenames[ caseType ]:
                   fn = self.dir + '/nwm.' + self.pdy + \
                                   '/' + caseType + '/' + f
                   #print fn
                   if not ( os.path.exists( fn ) and os.path.isfile( fn ) ):
                           missing.append( fn )
              return missing 

      def checkProducts( self, caseType ):
            missingfiles = self.missingProducts( caseType )
            if not missingfiles:
                    print( caseType + ' products OK!' )
            else:
                    if caseType == "usgs_timeslices" and \
                                    len( missingfiles ) < 8:
                            print( caseType + ' products OK!' )
                    else:     
                            print( caseType + ' has missing products:' )
#                            for f in missingfiles:
#                                    print "    " + f
       
      def getEachRFCTimeSeriesUniqueStations( self, rfcsites ):
              stapattern = '^.*/.*\.60min.([A-Z]{4}[0-9])\.RFCTimeSeries\.ncdf'
              rfcs = [ 'AB', 'SE', 'LM', 'MA', 'NE', 'WG', 'MB', 'CN', 'NW', \
                     'NC', 'CB', 'OH' ]

              #rfc_stations = dict.fromkeys( rfcs, set() )
              rfc_stations = dict( [ (r,set()) for r in rfcs ] )
              fn = self.dir + '/nwm.' + self.pdy + '/rfc_timeseries/' + \
                              self.filenames[ 'rfc_timeseries' ][ 0 ]
              for f in glob.glob( fn ):
                  idmatch = re.match( stapattern, f )
                  if idmatch:
                     if rfcsites.getRFCBySite( idmatch.groups()[0] ):
                        rfcname = \
                            rfcsites.getRFCBySite( idmatch.groups()[0] )[0:2]
                        rfc_stations[ rfcname ].add( idmatch.groups()[0] )

              return rfc_stations

      def getRFCTimeSeriesNumberOfStations( self ):
              fn = self.dir + '/nwm.' + self.pdy + '/rfc_timeseries/' + \
                              self.filenames[ 'rfc_timeseries' ][ 0 ]
              return [ ( self.pdy[:4]+'-'+self.pdy[4:6]+'-'+self.pdy[6:8]+'_' \
                         + self.cycle + ':00:00',  \
                         len( glob.glob( fn ) ) ) ]

      def getTimeSlicesNumberOfStations( self, caseType='usgs_timeslices'  ):
              if caseType == 'rfc_timeseries':
                 return self.getRFCTimeSeriesNumberOfStations()

              numofstations = []
              for f in self.filenames[ caseType ]:
                   fn = self.dir + '/nwm.' + self.pdy + \
                                   '/' + caseType + '/'+ f
                   nextday = datetime.strptime( self.pdy, "%Y%m%d" ) + \
                                   timedelta(days=1)

                   nextdayfn = self.dir + '/nwm.' + \
                                   nextday.strftime( "%Y%m%d" ) + \
                                   '/' + caseType + '/'+ f

                   if os.path.exists( nextdayfn ) and \
                                   os.path.isfile( nextdayfn ) :
                        fn = nextdayfn

                   if os.path.exists( fn ) and os.path.isfile( fn ) :
                      print("Found timeslice file: " + fn  )
                      prod = WRFHydroModelProduct( fn )
                      numofstations.append( \
                                      prod.getNumberOfStations( caseType ) )
                      prod.close()
                   else:
                      numofstations.append( \
                             ( f[:13] + ':' + f[14:16] + ':00', 0 ) )
                      print("No timeslice file: " + fn  )

              return numofstations

      def getUSGSStationRealTimeStreamFlow( self, stationId ):
              flows = []
              for f in self.filenames[ 'usgs_timeslices' ]:
                   fn = self.dir + '/nwm.' + self.pdy + \
                                   '/usgs_timeslices/'+ f
                   nextday = datetime.strptime( self.pdy, "%Y%m%d" ) + \
                                   timedelta(days=1)

                   nextdayfn = self.dir + '/nwm.' + \
                                   nextday.strftime( "%Y%m%d" ) + \
                                   '/usgs_timeslices/'+ f

                   if os.path.exists( nextdayfn ) and \
                                   os.path.isfile( nextdayfn ) :
                        fn = nextdayfn

                   #print fn
                   if os.path.exists( fn ) and os.path.isfile( fn ) :

                      prod = WRFHydroModelProduct( fn )
                      flow = prod.getUSGSStationRealTimeStreamFlow(\
                              stationId )
                      if flow: 
                        flows.append( flow )
                      prod.close()
              return flows

      def getUSGSStationRealTimeAllTimeStationStreamFlowQuality( self ):
              time_sta_flow_qual = {} 
              for f in self.filenames[ 'usgs_timeslices' ]:
                   fn = self.dir + '/nwm.' + self.pdy + \
                                   '/usgs_timeslices/'+ f
                   nextday = datetime.strptime( self.pdy, "%Y%m%d" ) + \
                                   timedelta(days=1)

                   nextdayfn = self.dir + '/nwm.' + \
                                   nextday.strftime( "%Y%m%d" ) + \
                                   '/usgs_timeslices/'+ f

                   if os.path.exists( nextdayfn ) and \
                                   os.path.isfile( nextdayfn ) :
                        fn = nextdayfn

                   print( fn )
                   if os.path.exists( fn ) and os.path.isfile( fn ) :

                      prod = WRFHydroModelProduct( fn )
                      centerTime = prod.getUSGSStationRealTimeCenterTime()
                      time_sta_flow_qual[ centerTime ] = \
                          prod.getUSGSStationRealTimeAllStationStreamFlowQuality()
                      prod.close()
              return time_sta_flow_qual

      def getStreamFlowByFeatureID( self, case, feaID, tmorf=0 ):
              time_flow = None
              dt = datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
              if case == 'analysis_assim' or \
                 case == 'analysis_assim_extend' or \
                 case == 'analysis_assim_long' or \
                 case == 'analysis_assim_hawaii' :
                      dt -= timedelta( hours = tmorf )
              else:
                      dt += timedelta( hours = tmorf )

              for f in self.filenames[ case ]:
                   fn = self.dir + '/nwm.' + self.pdy + \
                                   '/' + case + '/'+ f
                   if re.match( \
                      r'nwm.t[0-9][0-9]z\..*\.channel_rt(_[0-9])?\.(tm{0:02d}|f{0:03d})\.(conus|hawaii).nc'.format( tmorf ), f ):
                     if os.path.exists( fn ) and os.path.isfile( fn ) :

                        prod = WRFHydroModelProduct( fn )
                        flow = prod.getStreamFlowByFeatureID( feaID )
                        if flow: 
                          time_flow = (dt, flow )
                        prod.close()
                     break;
              return time_flow

      def getForecastStreamFlowByFeatureID( self, case, feaID ):
              time_flow = []
              dt = datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
              if case == 'analysis_assim':
                      start = 2 
                      step = -1
                      end = -1 
              elif case == 'analysis_assim_extend':
                      start = 27 
                      step = -1
                      end = -1 
              elif case == 'analysis_assim_long':
                      start = 11 
                      step = -1
                      end = -1 
              elif case == 'analysis_assim_hawaii':
                      start = 2
                      step = -1
                      end = -1 
              elif case == 'short_range':
                      start = 0 
                      step = 1
                      end = 19
              elif case == 'short_range_hawaii':
                      start = 0 
                      step = 1
                      end = 61
              elif case == 'medium_range_mem1' or \
                   case ==  'medium_range_mem2'        or \
                   case ==  'medium_range_mem3'        or \
                   case ==  'medium_range_mem4'        or \
                   case ==  'medium_range_mem5'        or \
                   case ==  'medium_range_mem6'        or \
                   case ==  'medium_range_mem7'        :
                      start = 0 
                      step = 3
                      end = 240
              elif case == 'long_range_mem1' or \
                   case == 'long_range_mem2' or \
                   case == 'long_range_mem3' or \
                   case == 'long_range_mem4':
                      start = 0 
                      step = 6 
                      end = 720
              else:
                      raise RuntimeError( "FATAL ERROR: Unknown caseType: " \
                        + case )

              for f in range(start, end, step ):
                  if case == 'analysis_assim':
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'analysis_assim.channel_rt.tm{0:02d}.conus.nc'.format( f )

                     timeofrec = dt - timedelta( hours = f )
                  elif case == 'analysis_assim_extend':
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'analysis_assim_extend.channel_rt.tm{0:02d}.conus.nc'.format( f )

                     timeofrec = dt - timedelta( hours = f )
                  elif case == 'analysis_assim_long':
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'analysis_assim_long.channel_rt.tm{0:02d}.conus.nc'.format( f )

                     timeofrec = dt - timedelta( hours = f )
                  elif case == 'analysis_assim_hawaii':
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'analysis_assim.channel_rt.tm{0:02d}.hawaii.nc'.format( f )

                     timeofrec = dt - timedelta( hours = f )
                  elif case == 'long_range_mem1' or \
                       case == 'long_range_mem2' or \
                       case == 'long_range_mem3' or \
                       case == 'long_range_mem4':
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'long_range.channel_rt_' + case[-1] + \
                      '.f{0:03d}.conus.nc'.format( f )

                     timeofrec = dt + timedelta( hours = f )

                  elif case == 'medium_range_mem1' or \
                       case ==  'medium_range_mem2'        or \
                       case ==  'medium_range_mem3'        or \
                       case ==  'medium_range_mem4'        or \
                       case ==  'medium_range_mem5'        or \
                       case ==  'medium_range_mem6'        or \
                       case ==  'medium_range_mem7'        :

                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'medium_range.channel_rt_' + case[-1] + \
                      '.f{0:03d}.conus.nc'.format( f )

                     timeofrec = dt + timedelta( hours = f )

                  elif case == 'short_range_hawaii':
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      'short_range.channel_rt.f{0:03d}.hawaii.nc'.format( f )

                     timeofrec = dt + timedelta( hours = f )
                  else:
                     fn = self.dir + '/nwm.' + self.pdy + \
                                     '/' + case + '/'+  \
                                   'nwm.t' + self.cycle + 'z.' + \
                      case + '.channel_rt.f{0:03d}.conus.nc'.format( f )

                     timeofrec = dt + timedelta( hours = f )

                  print( fn )
                  if os.path.exists( fn ) and os.path.isfile( fn ) :
                     prod = WRFHydroModelProduct( fn )
                     flow = prod.getStreamFlowByFeatureID( feaID )
                     print( "flow:", flow)
                     if flow: 
                        time_flow.append( (timeofrec, flow ) )
                     prod.close()
              print( time_flow )
              return time_flow

      def getVariable( self, case, type, var, tmorf=0 ):
              values = None
              domain = 'conus'
              if case[-6:] == 'hawaii':
                      domain = 'hawaii'

              if case[:8] == 'forcing_':
                 if case == 'forcing_analysis_assim' or\
                    case == 'forcing_analysis_assim_extend' or\
                    case == 'forcing_analysis_assim_hawaii' :
                         fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case[8:] + '.' + type + \
                              '.tm{0:02d}.' + domain + '.nc').format( tmorf )
                 else:
                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case[8:] + '.' + type + \
                              '.f{0:03d}.' + domain + '.nc').format( tmorf )
              else:

                 if case[:14] == 'analysis_assim':
                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                      case + '.' + type + \
                              '.tm{0:02d}.' + domain + '.nc').format( tmorf )
                 elif case == 'medium_range_mem1' or \
                      case ==  'medium_range_mem2'        or \
                      case ==  'medium_range_mem3'        or \
                      case ==  'medium_range_mem4'        or \
                      case ==  'medium_range_mem5'        or \
                      case ==  'medium_range_mem6'        or \
                      case ==  'medium_range_mem7'        or \
                      case ==  'long_range_mem1'        or \
                      case ==  'long_range_mem2'        or \
                      case ==  'long_range_mem3'        or \
                      case ==  'long_range_mem4' :

                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case[:-5] + '.' + type + '_' + case[-1] + \
                              '.f{0:03d}.' + domain + '.nc').format( tmorf )

                 else:
                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case + '.' + type + \
                              '.f{0:03d}.' + domain + '.nc').format( tmorf )

              if os.path.exists( fn ) and os.path.isfile( fn ) :

                        prod = WRFHydroModelProduct( fn )
                      
                        try:
                             values = prod.getVariable( var )

                        except RuntimeError as e:
                             raise e
              else:
                      raise RuntimeError( " file: " + fn + " does not exist!")

              return values 

      def getWRFHydroProd( self, case, type, var, tmorf=0 ):
              prod = None
              domain = 'conus'
              if case[-6:] == 'hawaii':
                      domain = 'hawaii'

              if case[:8] == 'forcing_':
                 if case == 'forcing_analysis_assim' or\
                    case == 'forcing_analysis_assim_extend' or\
                    case == 'forcing_analysis_assim_hawaii' :
                         fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case[8:] + '.' + type + \
                              '.tm{0:02d}.' + domain + '.nc').format( tmorf )
                 else:
                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case[8:] + '.' + type + \
                              '.f{0:03d}.' + domain + '.nc').format( tmorf )
              else:

                 if case[:14] == 'analysis_assim':
                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                      case + '.' + type + \
                              '.tm{0:02d}.' + domain + '.nc').format( tmorf )
                 elif case == 'medium_range_mem1' or \
                      case ==  'medium_range_mem2'        or \
                      case ==  'medium_range_mem3'        or \
                      case ==  'medium_range_mem4'        or \
                      case ==  'medium_range_mem5'        or \
                      case ==  'medium_range_mem6'        or \
                      case ==  'medium_range_mem7'        or \
                      case ==  'long_range_mem1'        or \
                      case ==  'long_range_mem2'        or \
                      case ==  'long_range_mem3'        or \
                      case ==  'long_range_mem4' :

                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case[:-5] + '.' + type + '_' + case[-1] + \
                              '.f{0:03d}.' + domain + '.nc').format( tmorf )

                 else:
                      fn = (self.dir + '/nwm.' + self.pdy + '/' + case +\
                                     '/nwm.t' + self.cycle + 'z.' + \
                                     case + '.' + type + \
                              '.f{0:03d}.' + domain + '.nc').format( tmorf )

              if os.path.exists( fn ) and os.path.isfile( fn ) :

                        prod = WRFHydroModelProduct( fn )
                      
              else:
                      raise RuntimeError( " file: " + fn + " does not exist!")

              return prod 
