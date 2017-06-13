import os
import re
import gzip
from datetime import datetime, timedelta
from string import *
from WRFHydroProduct import *


class NWMCom:

      def __init__(self, comDir, pdy, cycle ):
        self.dir = comDir 
        self.pdy = pdy 
        self.cycle = cycle
	self.filenames = dict( [ ('short_range', [] ), \
			         ('medium_range', [] ),\
				 ('long_range_mem1', []), \
				 ('long_range_mem2', []), \
				 ('long_range_mem3', []), \
				 ('long_range_mem4', []), \
				 ('analysis_assim', []), \
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
				 ('restart', []),            \
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
	      elif caseType == "medium_range":
                  for datatype in dataTypes:
                     for i in range(3, 243, 3):
	               self.filenames['medium_range'].append('nwm.t' + \
		            self.cycle + 'z.medium_range.' +\
			    datatype + '.f' + format( i, ">03") +     \
			    '.conus.nc' )

	      elif caseType == "analysis_assim":
                  for datatype in dataTypes:
                     for i in range(0, 3):
	                self.filenames['analysis_assim'].append('nwm.t' + \
		            self.cycle + 'z.analysis_assim.' +\
			    datatype + '.tm' + format( i, ">02" ) + \
			    '.conus.nc' )

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

	      elif caseType == "usgs_timeslices" :
                 dt = \
		  datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 for i in range(0, 4 ):
		    d = timedelta( minutes = i * 15 )
	            self.filenames['usgs_timeslices'].append(
		     ( dt +  d ).strftime( "%Y-%m-%d_%H:%M:00." ) + \
		     '15min.usgsTimeSlice.ncdf' )

	      elif caseType == "restart" :
                 dt = datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
                 self.filenames[ 'restart' ].append( 'nwm.rst.' + \
				     self.cycle + '/RESTART.' + \
                           self.pdy + self.cycle + '_DOMAIN1')

                 self.filenames[ 'restart' ].append( 'nwm.rst.' +   \
				     self.cycle + '/HYDRO_RST.' +       \
				     dt.strftime( "%Y-%m-%d_%H:00" ) \
                           + '_DOMAIN1' )

                 self.filenames[ 'restart' ].append( 'nwm.rst.' +   \
				self.cycle +                        \
				'/nudgingLastObs.' +                \
				dt.strftime( "%Y-%m-%d_%H:%M:00" )  \
				+ '.nc' )

              else:
		      raise RuntimeError( "FATAL ERROR: Unknown caseType: " \
			+ caseType )

#      def getFE_Long_Range_filenames( self, mem ):
#	    if mem < 5 and mem > 0 :
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
		  print file +'_rainrate'

      def thin_fe_products( self, caseType, thinvariable, outdir ): 
	      for f in self.filenames[caseType]:
                  fn = self.dir + '/nwm.' + self.pdy + \
				   '/' +caseType + '/' + f
		  outfn = self.unzip( fn, outdir )
		  prod = WRFHydroModelProduct( outfn )
		  print outfn
		  print outfn[:-3] + '.thinned.nc'
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
                    print caseType + ' products OK!'
            else:
		    if caseType == "usgs_timeslices" and \
				    len( missingfiles ) < 8:
                            print caseType + ' products OK!'
		    else:     
			    print caseType + ' has missing products:'
#			    for f in missingfiles:
#				    print "    " + f
       
      def getTimeSlicesNumberOfStations( self ):
	      numofstations = []
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
		      numofstations.append( \
				      prod.getNumberOfUSGSStations() )
		      prod.close()
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

      def getStreamFlowByFeatureID( self, case, feaID, tmorf=0 ):
	      time_flow = None
              dt = datetime.strptime( self.pdy+self.cycle, "%Y%m%d%H" )
	      if case == 'analysis_assim':
		      dt -= timedelta( hours = tmorf )
	      else:
		      dt += timedelta( hours = tmorf )

              for f in self.filenames[ case ]:
                   fn = self.dir + '/nwm.' + self.pdy + \
				   '/' + case + '/'+ f
		   if re.match( \
		      r'nwm.t[0-9][0-9]z\..*\.channel_rt\.(tm{0:02d}|f{0:03d})\.conus.nc'.format( tmorf ), f ):
		     print fn
		     if os.path.exists( fn ) and os.path.isfile( fn ) :

                        prod = WRFHydroModelProduct( fn )
	   	        flow = prod.getStreamFlowByFeatureID( feaID )
		        if flow: 
                          print 'flow = ', flow
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
	      elif case == 'short_range':
		      start = 0 
		      step = 1
                      end = 19
	      elif case == 'medium_range':
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

	          else:
                     fn = self.dir + '/nwm.' + self.pdy + \
				     '/' + case + '/'+  \
				   'nwm.t' + self.cycle + 'z.' + \
                      case + '.channel_rt.f{0:03d}.conus.nc'.format( f )

		     timeofrec = dt + timedelta( hours = f )

                  print ('fn = ', fn )
		  if os.path.exists( fn ) and os.path.isfile( fn ) :

                     prod = WRFHydroModelProduct( fn )
	   	     flow = prod.getStreamFlowByFeatureID( feaID )
		     if flow: 
		        time_flow.append( (timeofrec, flow ) )
		     prod.close()

              return time_flow
