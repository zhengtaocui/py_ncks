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
   startday = ''
   endday = ''
   try:
      opts, args = \
	 getopt.getopt(argv,"hd:s:e:",["dir=", "startday=", "endday=" ])
   except getopt.GetoptError:
      print \
        'checkUSGSStatationNumbers.py -d <comdir> -s <startpdy> -e <endpdy>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print  \
           'checkUSGSStatationNumbers.py -d <comdir> -s <startpdy> -e <endpdy>' 
         sys.exit()
      elif opt in ('-d', "--dir"):
         comdir = arg
         if not os.path.exists( comdir ):
           if not os.path.isdir( comdir ):
             print 'com dir ', comdir, ' does not exist!'
             sys.exit()
      elif opt in ('-s', "--startpdy" ):
         startday = arg
      elif opt in ('-e', "--endday" ):
         endday=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'

   return (comdir, startday, endday)


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
startpdy = datetime.strptime( pgmopt[1], "%Y%m%d" )
endpdy = datetime.strptime( pgmopt[2], "%Y%m%d" )

timeslices = []
oneday = timedelta( days = 1)

flow = []
simdFlowtm0 = []
simdFlowtm1 = []
simdFlowtm2 = []
fcstFlowt00z = []
fcstFlowAnAt00z = []
fcstFlowLR1t00z = []
fcstFlowMRt00z = []

dateiter = startpdy

feaid = OneDayNWMCom.getForecastPointByUSGSStation( "/gpfs/hps/nwc/noscrub/Brian.Cosgrove/nwm_parm.v1.2/1.2/domain/RouteLink_NHDPLUS.nc", "07064533" )
print "feaid = ", feaid

startCom = OneDayNWMCom( comdir, startpdy.strftime(  "%Y%m%d" ) )

fcstFlowt00z = startCom.getForecastStreamFlowByFeatureID( 'short_range', \
		    feaid, 2 )
fcstFlowAnAt00z = startCom.getForecastStreamFlowByFeatureID( 'analysis_assim', \
		    feaid, 2 )
fcstFlowLR1t00z = startCom.getForecastStreamFlowByFeatureID( 'long_range_mem1', \
		    feaid, 6 )
fcstFlowMRt00z = startCom.getForecastStreamFlowByFeatureID( 'medium_range', \
		    feaid, 6 )

print 'fcstFlowt00z:', fcstFlowt00z
print 'fcstFlowAnAt00z:', fcstFlowAnAt00z
print 'fcstFlowLR1t00z:', fcstFlowLR1t00z
print 'fcstFlowMRt00z:', fcstFlowMRt00z


while dateiter < endpdy:

    com = OneDayNWMCom( comdir, dateiter.strftime(  "%Y%m%d" ) )
		            
#    com.getForecastPoint( "/gpfs/hps/nwc/noscrub/Brian.Cosgrove/nwm_parm.v1.2/1.2/template/WRF_Hydro_NWM_v1.1_geospatial_data_template_channel_point_netcdf.nc", [37.37569444, -91.5528056] )


    simdFlowtm0 += com.getStreamFlowByFeatureID( 'analysis_assim', feaid, 0 )
    simdFlowtm1 += com.getStreamFlowByFeatureID( 'analysis_assim', feaid, 1 )
    simdFlowtm2 += com.getStreamFlowByFeatureID( 'analysis_assim', feaid, 2 )

    flow += com.getUSGSStationRealTimeStreamFlow("07064533")

    dateiter += oneday

#print simdFlow

flow_date = []
flow_value = []

for f in flow:
   flow_value.append( f[1] )
   flow_date.append( datetime.strptime( f[0], "%Y-%m-%d_%H:%M:%S" ) )

simdflowtm0_date = []
simdflowtm0_value = []
simdflowtm1_date = []
simdflowtm1_value = []
simdflowtm2_date = []
simdflowtm2_value = []

for f in simdFlowtm0:
   print ( f )
   simdflowtm0_value.append( f[1] )
   print f[0], f[1]
   simdflowtm0_date.append( f[0] )

print simdFlowtm1
for f in simdFlowtm1:
   print ( f )
   simdflowtm1_value.append( f[1] )
   print f[0], f[1]
   simdflowtm1_date.append( f[0] )

for f in simdFlowtm2:
   print ( f )
   simdflowtm2_value.append( f[1] )
   print f[0], f[1]
   simdflowtm2_date.append( f[0] )

fig = Figure()
canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)

dischargeplot, = ax.plot( [i[0] for i in fcstFlowt00z], \
		          [i[1] for i in fcstFlowt00z], \
			  linestyle='--', \
	marker=None, color='k', label='SR t02z')
dischargeplot, = ax.plot( [i[0] for i in fcstFlowMRt00z], \
		          [i[1] for i in fcstFlowMRt00z], \
			  linestyle='-.', \
	marker=None, color='k', label='MR t02z')
dischargeplot, = ax.plot( [i[0] for i in fcstFlowLR1t00z], \
		          [i[1] for i in fcstFlowLR1t00z], \
			  linestyle=':', \
	marker=None, color='k', label='LR1 t02z')

dischargeplot, = ax.plot( flow_date, flow_value, linestyle='', \
	marker='o', markersize=3, markerfacecolor='None', color='k',\
        label='USGS Obv')

dischargeplot, = ax.plot( simdflowtm0_date, simdflowtm0_value, linestyle='-', \
	marker='x', markersize=3, markerfacecolor='None', color='k', \
	label='AnA tm00')

dischargeplot, = ax.plot( simdflowtm1_date, simdflowtm1_value, linestyle='-', \
	marker='*', markersize=3, markerfacecolor='None', color='k', \
	label='AnA tm01')

dischargeplot, = ax.plot( simdflowtm2_date, simdflowtm2_value, linestyle='-', \
	marker='v', markersize=3, markerfacecolor='None', color='k', \
	label='AnA tm02')

ax.xaxis.set_major_locator( mdates.DayLocator() )
ax.xaxis.set_minor_locator( mdates.HourLocator() )

ax.set_xlim( startpdy, endpdy )
fig.autofmt_xdate()

ax.grid( True )
ax.xaxis.set_major_formatter( mdates.DateFormatter('%b %d' ))

ax.set_title( 'USGS 07064533' )
ax.set_xlabel( '2017' )
ax.set_ylabel( 'Streamflow($\mathsf{m^3/s}$)' )
ax.legend()

canvas.print_figure('USGS_07064533_stream_flow.pdf')

#cleaning up

