#!/usr/bin/env python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
import numpy as np 
from string import *

def main(argv):
   """
     function to get input arguments
   """
   inputdir = ''
   outputdir = ''
   try:
           opts, args = getopt.getopt(argv,"hi:j:v:t:",["file1=", "file2=", "var=", "tol=" ])
   except getopt.GetoptError:
      print( 'diffnc.py -i <input1> -j <input2> -v <variable> -t <tolerance>' )
      sys.exit(2)
   for opt, arg in opts:
      print( opt, arg )
      if opt == '-h':
         print(   \
          'diffnc.py -i <input1> -j <input2> -v <variable> -t <tolerance>'  )
         sys.exit()
      elif opt in ('-i', "--file1"):
         input1 = arg
         if not os.path.exists( input1 ):
           if not os.path.isfile( input1 ):
             print( 'input dir ', input1, ' does not exist!' )
             sys.exit()
      elif opt in ('-j', "--file2"):
         input2 = arg
         if not os.path.exists( input2 ):
           if not os.path.isfile( input2 ):
             print( 'input dir ', input2, ' does not exist!' )
             sys.exit()
      elif opt in ('-v', "--var" ):
         var = arg
      elif opt in ('-t', "--tal" ):
         tol = arg
  
   print( 'file1 is "', input1, '"' )
   print( 'file2 is "', input2, '"' )
   print( 'variable is "', var, '"' )
   print( 'tolerance is "', tol , '"' )

   return (input1, input2, var, tol)



if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

file1 = pgmopt[0]
file2 = pgmopt[1]
var = pgmopt[2]
tol = float( pgmopt[3] )

print( file1, file2, var, tol )

ds1 = netCDF4.Dataset( file1, 'r' )
ds2 = netCDF4.Dataset( file2, 'r' )

var1 = ds1.variables[ var ]
var2 = ds2.variables[ var ]

#
# check shapes
#
isShapeSame = all(map(lambda i, j: i == j, var1.shape, var2.shape) )

if not isShapeSame:
    print( 'NetCDF files have different shapes!' )
    sys.exit(1)

print( var1.shape )


diff = np.subtract( var1, var2 )

#np.set_printoptions(threshold=sys.maxsize)

for d in diff.flat:
  if abs(d) >= tol:
    print(d)

print( "Max diff: ", np.max( diff ) )
print( "Min diff: ", np.min( diff ) )
