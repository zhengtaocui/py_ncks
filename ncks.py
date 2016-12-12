#! /usr/bin/python

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
	   opts, args = getopt.getopt(argv,"hi:o:",["id=", "od=" ])
   except getopt.GetoptError:
      print 'ncks.py -i <inputdir> -o <outputdir>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print   \
          'ncks.py -i <inputdir> -o <outputdir>' 
         sys.exit()
      elif opt in ('-i', "--id"):
         inputdir = arg
         if not os.path.exists( inputdir ):
           if not os.path.isdir( inputdir ):
             print 'input dir ', inputdir, ' does not exist!'
             sys.exit()
      elif opt in ('-o', "--od" ):
         outputdir = arg
         if not os.path.exists( os.path.dirname( outputdir ) ):
             print 'output dir ', os.path.dirname( outputdir), \
			      ' does not exist!'
             sys.exit()
  
   print 'input dir is "', inputdir, '"'
   print 'output dir is "', outputdir, '"'

   return (inputdir, outputdir)

def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True


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


def create_outputdir_and_get_list_of_files( indir, outdir, cases, datetimetag):

  allfiles = []
  for case in cases:
     nwmdir =  indir + '/nwm.' + datetimetag + '/' + case
     nwmoutdir = outdir + '/nwm.' + datetimetag + '/' + case

     print "nwmdir = ", nwmdir
     print "nwmoutdir = ", nwmoutdir

     if not os.path.isdir( nwmdir ):
	  continue

     if not os.path.isdir( nwmoutdir ):
	  os.makedirs( nwmoutdir )
      
     chn_and_land_files = [ f for f in os.listdir( nwmdir ) \
		   if re.match( \
	   r'nwm.t[0-9]{2}z\..*(channel_rt|land)(_[0-9])?\.(tm00|f[0-9]{3})\.conus.nc(.gz)?',\
                    f ) ]

     for file in chn_and_land_files:
       print "create_outputdir_and_get_list_of_files:", file
       allfiles.append( '/nwm.' + datetimetag + '/' + case +'/' + file )

  return allfiles

#
# delete files older than number of days in a given directory
#
def cleanup_dir( path, numberofdays ):
   if not os.path.isdir(path ):
         return

   now = time.time()
   cutoff = now - ( numberofdays * 86400 )
   files = os.listdir( path )
   for onefile in files:
         if os.path.isfile( path + '/' + onefile ):
                 t = os.stat( path + '/' + onefile )
                 c = t.st_mtime
                 if c < cutoff :
                    os.remove( path + '/' + onefile )
   return


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

indir = pgmopt[0]
outdir = pgmopt[1]

#cleaning up
for root, dirs, files in os.walk( outdir ):
     for dir in dirs:
        cleanup_dir( os.path.join( root, dir) , 2 )
	try:
	  print 'remove: ' , os.path.join( root, dir )
          os.rmdir( os.path.join( root, dir ) )
        except Exception:
          pass

cases = ['analysis_assim', 'short_range', 'medium_range', 'long_range_mem1', \
		'long_range_mem2', 'long_range_mem3', 'long_range_mem4' ]


dttag = time.strftime("%Y%m%d", time.gmtime() )

allfilestocheck = create_outputdir_and_get_list_of_files( indir, outdir, cases, dttag )

if int( time.strftime("%H", time.gmtime() ) ) < 6  :
   dttag = time.strftime("%Y%m%d", time.gmtime( time.time() - 3 * 3600 ) )
   predayallfilestocheck = \
      create_outputdir_and_get_list_of_files( indir, outdir, cases, dttag )

   for file in predayallfilestocheck:
      allfilestocheck.append( file )

for file in allfilestocheck:

   t = os.stat( indir + file )
   c = t.st_ctime

   if c >= time.time() - 3 * 3600 :
      print "copying : ", indir + file
      shutil.copyfile( indir + file, outdir + file )

      if re.match( \
         r'.*/nwm.t[0-9]{2}z\..*land(_[0-9])?\.(tm00|f[0-9]{3})\.conus.nc(.gz)?', file ) :
         if file.endswith( '.gz' ):
           inF = gzip.open( outdir+file, 'rb' )
	   outF = open( outdir + file[:-3], 'wb' )
           file_content = inF.read()
           inF.close()
           outF.write( file_content )
           outF.close()
	   prod = WRFHydroModelProduct(  outdir + file[:-3] )
	   print 'thin: ', outdir + file[:-3]
           prod.thinToVariable( 'SOILSAT_TOP', outdir + file[:-6] + '.thinned.nc' )
	   os.remove( outdir + file )
	   os.remove( outdir + file[:-3] )
	   inFThined = open(  outdir + file[:-6] + '.thinned.nc', 'rb' )
	   outFThined = gzip.open( outdir + file[:-6] + '.thinned.nc.gz', 'wb' )
	   outFThined.writelines( inFThined )
	   outFThined.close()
	   inFThined.close()
	   os.remove( outdir + file[:-6] + '.thinned.nc'  )
         else:
	   prod = WRFHydroModelProduct(  outdir + file )
	   print 'thin: ', outdir + file[:-3]
           prod.thinToVariable( 'SOILSAT_TOP', outdir + file[:-3] + '.thinned.nc' )
	   os.remove( outdir + file )
	   inFThined = open(  outdir + file[:-3] + '.thinned.nc', 'rb' )
	   outFThined = gzip.open( outdir + file[:-3] + '.thinned.nc.gz', 'wb' )
	   outFThined.writelines( inFThined )
	   outFThined.close()
	   inFThined.close()
	   os.remove( outdir + file[:-3] + '.thinned.nc'  )

