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
   usgsSta = ''
   rutlnk =  "/gpfs/hps/nwc/noscrub/Zhengtao.Cui/nwm_parm.v1.2/1.2/domain/RouteLink_NHDPLUS.nc" 
   tm0=None
   tm1=None
   tm2=None
   anapdycyc = None
   srpdycyc = None
   mrpdycyc = None
   lr1pdycyc = None
   lr2pdycyc = None
   lr3pdycyc = None
   lr4pdycyc = None
   title = None
   output=None
   try:
	   opts, args = getopt.getopt(argv,"hd:s:e:u:r:o:",\
		      ["dir=", "startday=", "endday=", "usgsid=", "rutlnk=",\
		      "tm0=", "tm1=", "tm2=","ana=", "sr=", "mr=", "lr1=", \
		      "lr2=", "lr3=", "lr4=", \
		      "title=", "output="])
   except getopt.GetoptError:
      print \
        'plotStreamFlow.py -d <comdir> -s <startpdy> -e <endpdy> -r <rutlnk> --sr <pdycyc> --mr <pdycyc> --lr1 <pdycyc> --lr2 <pdycyc> --lr3 <pdycyc> --lr4 <pdycyc> --title <title>'

      sys.exit(2)

   if not opts:
      print \
        'plotStreamFlow.py -d <comdir> -s <startpdy> -e <endpdy> -r <rutlnk> --sr <pdycyc> --mr <pdycyc> --lr1 <pdycyc> --lr2 <pdycyc> --lr3 <pdycyc> --lr4 <pdycyc> --title <title>'
      sys.exit(2)

   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print  \
        'plotStreamFlow.py -d <comdir> -s <startpdy> -e <endpdy> -r <rutlnk> --sr <pdycyc> --mr <pdycyc> --lr1 <pdycyc> --lr2 <pdycyc> --lr3 <pdycyc> --lr4 <pdycyc> --title <title>'
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
      elif opt in ('-u', "--usgsid" ):
         usgsSta=arg
      elif opt in ('-r', "--rutlnk" ):
         rutlnk=arg
      elif opt in ("--tm0" ):
         if arg:
           tm0 = arg
         else:
           tm0 = startday + '00'
      elif opt in ("--tm1" ):
         if arg:
           tm1 = arg
         else:
           tm1 = startday + '00'
      elif opt in ("--tm2" ):
         if arg:
           tm2 = arg
         else:
           tm2 = startday + '00'
      elif opt in ("--ana" ):
         anapdycyc=arg.split(',')
      elif opt in ("--sr" ):
         srpdycyc=arg.split(',')
      elif opt in ("--mr" ):
         mrpdycyc=arg.split(',')
      elif opt in ("--lr1" ):
         lr1pdycyc=arg.split(',')
      elif opt in ("--lr2" ):
         lr2pdycyc=arg.split(',')
      elif opt in ("--lr3" ):
         lr3pdycyc=arg.split(',')
      elif opt in ("--lr4" ):
         lr4pdycyc=arg.split(',')
      elif opt in ("--title" ):
         title=arg
      elif opt in ('-o', "--output" ):
         output=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'
   return (comdir, startday, endday, usgsSta, rutlnk, tm0, tm1, tm2, anapdycyc,\
		   srpdycyc, mrpdycyc,\
		   lr1pdycyc, lr2pdycyc, lr3pdycyc, lr4pdycyc, title, output )


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
startpdy = datetime.strptime( pgmopt[1], "%Y%m%d" )
endpdy = datetime.strptime( pgmopt[2], "%Y%m%d" )
usgsSta = pgmopt[3]
rutlnk = pgmopt[4]
tm0 = pgmopt[5]
tm1 = pgmopt[6]
tm2 = pgmopt[7]
ana = pgmopt[8]
sr = pgmopt[9]
mr = pgmopt[10]
lr1 = pgmopt[11]
lr2 = pgmopt[12]
lr3 = pgmopt[13]
lr4 = pgmopt[14]
xtitle = pgmopt[15]
outfile = pgmopt[16]

timeslices = []
oneday = timedelta( days = 1)

flow = []
simdFlowtm0 = []
simdFlowtm1 = []
simdFlowtm2 = []
fcstFlowAAt00z = []
fcstFlowSRt00z = []
fcstFlowLR1t00z = []
fcstFlowLR2t00z = []
fcstFlowLR3t00z = []
fcstFlowLR4t00z = []
fcstFlowMRt00z = []

dateiter = startpdy

if tm0 is not None:
  tm0dt = datetime.strptime( tm0, "%Y%m%d%H" )
if tm1 is not None:
  tm1dt = datetime.strptime( tm1, "%Y%m%d%H" )
if tm2 is not None:
  tm2dt = datetime.strptime( tm2, "%Y%m%d%H" )

feaid = OneDayNWMCom.getForecastPointByUSGSStation( rutlnk, usgsSta )

print "feaid = ", feaid

startCom = OneDayNWMCom( comdir, startpdy.strftime(  "%Y%m%d" ) )
if ana is not None:
	for c in ana:
            srCom = OneDayNWMCom( comdir, ana[:8] ) 
            fcstFlowAAt00z.append( \
	       srCom.getForecastStreamFlowByFeatureID( 'analysis_assim', \
		  feaid, int( ana[8:]) ) )

if sr is not None:
	for c in sr:
            srCom = OneDayNWMCom( comdir, c[:8] ) 
            fcstFlowSRt00z.append( \
	       srCom.getForecastStreamFlowByFeatureID( 'short_range', \
		  feaid, int( c[8:]) ) )
#  print "fcstFlowSRt00z: ", fcstFlowSRt00z

if mr is not None:
	for c in mr:
          mrCom = OneDayNWMCom( comdir, c[:8] ) 
          fcstFlowMRt00z.append( \
	     mrCom.getForecastStreamFlowByFeatureID( 'medium_range', \
		  feaid, int( c[8:]) ) )

if lr1 is not None:
	for c in lr1:
          lr1Com = OneDayNWMCom( comdir, c[:8] ) 
          fcstFlowLR1t00z.append( \
	     lr1Com.getForecastStreamFlowByFeatureID( 'long_range_mem1', \
		  feaid, int( c[8:]) ) )

if lr2 is not None:
	for c in lr2:
          lr2Com = OneDayNWMCom( comdir, c[:8] ) 
          fcstFlowLR2t00z.append( \
		  lr2Com.getForecastStreamFlowByFeatureID( \
		  'long_range_mem2', feaid, int( c[8:]) ) )

if lr3 is not None:
	for c in lr3:
          lr3Com = OneDayNWMCom( comdir, c[:8] ) 
          fcstFlowLR3t00z.append( \
		  lr3Com.getForecastStreamFlowByFeatureID( \
		  'long_range_mem3', feaid, int( c[8:]) ) )
if lr4 is not None:
	for c in lr4:
          lr4Com = OneDayNWMCom( comdir, c[:8] ) 
          fcstFlowLR4t00z.append( \
			  lr4Com.getForecastStreamFlowByFeatureID( \
		  'long_range_mem4', feaid, int( c[8:]) ) )

#print 'fcstFlowLR1t00z:', fcstFlowLR1t00z
#print 'fcstFlowMRt00z:', fcstFlowMRt00z

while dateiter < endpdy:

    com = OneDayNWMCom( comdir, dateiter.strftime(  "%Y%m%d" ) )
		            
#    com.getForecastPoint( "/gpfs/hps/nwc/noscrub/Brian.Cosgrove/nwm_parm.v1.2/1.2/template/WRF_Hydro_NWM_v1.1_geospatial_data_template_channel_point_netcdf.nc", [37.37569444, -91.5528056] )

    if tm0 is not None and dateiter >= tm0dt:
       simdFlowtm0 += com.getStreamFlowByFeatureID( 'analysis_assim', feaid, 0 )
    if tm1 is not None and dateiter >= tm1dt:
       simdFlowtm1 += com.getStreamFlowByFeatureID( 'analysis_assim', feaid, 1 )
    if tm2 is not None and dateiter >= tm2dt:
       simdFlowtm2 += com.getStreamFlowByFeatureID( 'analysis_assim', feaid, 2 )

    flow += com.getUSGSStationRealTimeStreamFlow( usgsSta )

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


fig = Figure(figsize=(3*4,3*3))

canvas = FigureCanvas(fig)

ax = fig.add_subplot(111)

if ana is not None:
	for f, c in  zip( fcstFlowAAt00z, ana ):
          dischargeplot, = ax.plot( [i[0] for i in f], [i[1] for i in f], \
			  linestyle='.', \
	  marker=None, color='k', label='AnA ' + c )

if sr is not None:
	for f, c in  zip( fcstFlowSRt00z, sr ):
          dischargeplot, = ax.plot( [i[0] for i in f], [i[1] for i in f], \
			  linestyle='--', \
	  marker=None, color='k', label='SR ' + c )

if mr is not None:
	for f, c in  zip( fcstFlowMRt00z, sr ):
          dischargeplot, = ax.plot( [i[0] for i in f], \
		          [i[1] for i in f], \
			  linestyle='-.', \
	  marker=None, color='k', label='MR ' + c)

if lr1 is not None:
	for f, c in  zip( fcstFlowLR1t00z, lr1 ):
          dischargeplot, = ax.plot( [i[0] for i in f], \
		          [i[1] for i in f], \
			  linestyle=':', \
	  marker="o", color='k', label='LR1 ' + c)

if lr2 is not None:
	for f, c in  zip( fcstFlowLR2t00z, lr2 ):
          dischargeplot, = ax.plot( [i[0] for i in f], \
		          [i[1] for i in f], \
			  linestyle=':', \
	  marker="v", color='k', label='LR2 ' + c)

if lr3 is not None:
	for f, c in  zip( fcstFlowLR3t00z, lr3 ):
          dischargeplot, = ax.plot( [i[0] for i in f], \
		          [i[1] for i in f], \
			  linestyle=':', \
   	   marker="x", color='k', label='LR3 ' + c)

if lr4 is not None:
	for f, c in  zip( fcstFlowLR3t00z, lr4 ):
          dischargeplot, = ax.plot( [i[0] for i in f], \
		          [i[1] for i in f], \
			  linestyle=':', \
	    marker="s", color='k', label='LR4 ' + c)

dischargeplot, = ax.plot( flow_date, flow_value, linestyle='', \
	marker='o', markersize=3, markerfacecolor='None', color='k',\
        label='USGS Obv')

if tm0 is not None:
      dischargeplot, = ax.plot( simdflowtm0_date, simdflowtm0_value, linestyle='-', \
	marker='x', markersize=3, markerfacecolor='None', color='k', \
	label='AnA tm00')

if tm1 is not None:
      dischargeplot, = ax.plot( simdflowtm1_date, simdflowtm1_value, linestyle='-', \
	marker='*', markersize=3, markerfacecolor='None', color='k', \
	label='AnA tm01')

if tm2 is not None:
      dischargeplot, = ax.plot( simdflowtm2_date, simdflowtm2_value, linestyle='-', \
	marker='v', markersize=3, markerfacecolor='None', color='k', \
	label='AnA tm02')

ax.xaxis.set_major_locator( mdates.DayLocator() )
ax.xaxis.set_minor_locator( mdates.HourLocator() )

ax.set_xlim( startpdy, endpdy )
fig.autofmt_xdate()

ax.grid( True )
ax.xaxis.set_major_formatter( mdates.DateFormatter('%b %d' ))

if xtitle is not None:
   ax.set_title( xtitle )
else:  
   ax.set_title( 'USGS ' + usgsSta )

if startpdy.year == endpdy.year:
   ax.set_xlabel( startpdy.strftime(  "%Y" ) )
else:
   ax.set_xlabel( startpdy.strftime(  "%Y" ) + '-' + endpdy.strftime(  "%Y" ) )

ax.set_ylabel( 'Streamflow($\mathsf{m^3/s}$)' )
ax.legend()

if outfile is not None:
   canvas.print_figure( outfile + '.pdf' )
else:
   canvas.print_figure('USGS_' + usgsSta + '_stream_flow.pdf')

#cleaning up
