#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
import numpy as np 
from string import *
import matplotlib as mpl
mpl.use('Agg')
from mpl_toolkits.basemap import Basemap, cm
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MultipleLocator, FormatStrFormatter, Formatter
from matplotlib.ticker import FuncFormatter
#from cycler import cycler

from OneDayNWMCom import *

def frange(start, stop, step):
     i = start
     while i < stop:
         yield i
         i += step

def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    elif n == 1:
        return([start])
    else:
        return([])

def main(argv):
   """
     function to get input arguments
   """
   comdir = ''
   pdycyc = None
   case = None
   type = None
   var = None
   tmorf = None
   start = None
   stop = None
   step = None
   title = None
   output="NWM_grid"
   try:
	   opts, args = getopt.getopt(argv,"hd:p:c:t:v:f:",\
		      ["dir=", "pdycyc=", \
		      "case=", "type=", "var=", "tmorf=", \
		      "start==", "stop=", "step=", \
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
      elif opt in ('-p', "--pdycyc" ):
         pdycyc = arg
      elif opt in ('-c', "--case" ):
         case=arg
      elif opt in ('-t', "--type" ):
         type=arg
      elif opt in ('-v', "--var" ):
         var=arg
      elif opt in ('-f', "--tmorf" ):
         tmorf=arg
      elif opt in ("--start" ):
         start=arg
      elif opt in ("--stop" ):
         stop=arg
      elif opt in ("--step" ):
         step=arg
      elif opt in ("--title" ):
         title=arg
      elif opt in ('-o', "--output" ):
         output=arg
  
#   print 'com dir is "', comdir, '"'
#   print 'pdy is "', pdy, '"'
#   print 'cyc is "', cycle, '"'
   return (comdir, pdycyc, case, type, var, tmorf, start, stop, step, title, output )


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

comdir = pgmopt[0]
pdy = pgmopt[1][:8]
cycle = int( pgmopt[1][8:] )
case = pgmopt[2]
type = pgmopt[3]
var = pgmopt[4]
tmorf = pgmopt[5]
start = pgmopt[6]
stop = pgmopt[7]
step = pgmopt[8]
xtitle = pgmopt[9]
outfile = pgmopt[10]

print comdir, pdy, cycle, case, type, var, tmorf, start, stop, step, xtitle, outfile

varValues = []

com = OneDayNWMCom( comdir, pdy )

varValues = com.getVariable( case, type, cycle, var,  int( tmorf ) )

x = com.getVariable( case, type, cycle, 'x',  int( tmorf ) )
y = com.getVariable( case, type, cycle, 'y',  int( tmorf ) )

minValue = max( map( max, varValues ) )
minValue = min( map( min, varValues ) )

print "Max value: ", max( map( max, varValues ) )
print "Min value: ", min( map( min, varValues ) )
print x[0], x[-1]
print y[0], y[-1]
print x,y

atts_units = com.getComCycle( cycle ).getWRFHydroProd( \
		      case, type, var, int( tmorf ) ).getVariableAttributes( \
		      var, 'units' )
print atts_units

atts_longname = com.getComCycle( cycle ).getWRFHydroProd( \
		      case, type, var, int( tmorf ) ).getVariableAttributes( \
		      var, 'long_name' )

fig = plt.figure( figsize=(8,8))
ax = fig.add_axes([0.1,0.1,0.8,0.8])

if xtitle:
   #fig.suptitle( xtitle )
   ax.set_title( xtitle )

width = x[-1] - x[ 0 ] + ( x[1] - x[0] )
height = y[-1] - y[ 0 ] + ( y[1] - y[0] )
m = Basemap( projection='lcc', rsphere=(6370000,6370000), \
		resolution='c', area_thresh=10000., \
		lat_1=30., lat_2=60., lat_0=40., lon_0=-97, \
		width=width, height=height )
m.drawcoastlines()
m.drawstates()
m.drawcountries()
parallels = np.arange(0.,90,10.)
m.drawparallels( parallels, labels=[1,0,0,0], fontsize=10 )
meridians = np.arange(180,360,10)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

x0 = abs( x[0] )
y0 = abs( y[0] )

x += x0
y += y0

X,Y = np.meshgrid( x, y )

print X, Y

print x.shape[0]
print y.shape[0]
#print seq(0.0, 0.035, 0.001)

if start and stop and step:
   cs = m.contourf( X, Y, varValues[0], levels=seq(start, stop, step), cmap=cm.s3pcpn )
else:
   cs = m.contourf( X, Y, varValues[0], 20, cmap=cm.s3pcpn )
#cs = m.pcolormesh(X,Y,np.squeeze( varValues[0] ), cmap=cm.s3pcpn)

cbar = m.colorbar(cs, location='bottom', pad="10%")
cbar.set_label( atts_longname + '(' + atts_units + ')' + ' : Max=' + str( maxValue) + ' : Min=' \
		+ str(minValue) )

fig.savefig(outfile + '.pdf', bbox_inches='tight')


#cleaning up

