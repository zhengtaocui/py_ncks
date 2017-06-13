#! /usr/bin/python

import os, sys, time, urllib, getopt, copy
import gzip, shutil, re
import netCDF4     
import numpy as np 
from string import *
from datetime import datetime, timedelta
from sets import Set

def main(argv):
   """
     function to get input arguments
   """
   inputdir = ''
   outputdir = ''
   startdate = ''
   enddate = ''
   try:
	   opts, args = getopt.getopt(argv,"hi:o:s:e:",["id=", "od=", "start=", "end=" ])
   except getopt.GetoptError:
      print 'ncks_retro.py -i <inputdir> -o <outputdir> -s <startdate> -e <enddate>' 
      sys.exit(2)
   for opt, arg in opts:
      print opt, arg
      if opt == '-h':
         print 'ncks_retro.py -i <inputdir> -o <outputdir> -s <startdate> -e <enddate>' 
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
      elif opt in ('-s', "--sd" ):
         startdate = arg
      elif opt in ('-e', "--ed" ):
         enddate = arg
  
   print 'input dir is "', inputdir, '"'
   print 'output dir is "', outputdir, '"'
   print 'startdate is "', startdate, '"'
   print 'enddate is "', enddate, '"'

   return (inputdir, outputdir, startdate, enddate)

def file_accessible(filepath, mode):
    ''' Check if a file exists and is accessible. '''
    try:
        f = open(filepath, mode)
        f.close()
    except IOError as e:
        return False

    return True

def maybe_encode(string, encoding='ascii'):
    try:
       return string.encode(encoding)
    except ( UnicodeEncodeError, AttributeError ):
       return string

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

	      atts = dict()
	      for vattname in variable.ncattrs() :
	         #x.setncattr( vattname, maybe_encode( variable.getncattr( vattname ) ) )
	         #x.setncattr( vattname, variable.getncattr( vattname ) )
		 att = maybe_encode( variable.getncattr( vattname ) )
		 atts[ vattname ] = att

              x.setncatts( atts )
              outnc.variables[name][:] = self.nc_fid.variables[name][:]

	atts = dict()
	for name in self.nc_fid.ncattrs():
            att = self.nc_fid.getncattr( name )
	    atts[ name ] = maybe_encode( att )
	    #outnc.setncattr( name,  maybe_encode( self.nc_fid.getncattr( name ) ) )
	    #outnc.setncattr( name,  self.nc_fid.getncattr( name ) )
        outnc.setncatts( atts )

        outnc.close()

      def thinToVariables(self, varnames, outncfilename ):

        outnc = netCDF4.Dataset( outncfilename, "w", format=self.nc_fid.data_model )

        for name, dimension in self.nc_fid.dimensions.iteritems():
	  outnc.createDimension(name, len(dimension) \
			  if not dimension.isunlimited() else None)

	for name, variable in self.nc_fid.variables.iteritems():
	    # take out the variable you don't want
	    if name in varnames: 
              x = outnc.createVariable( name, variable.datatype, \
			    variable.dimensions, zlib = True, complevel = 2)

	      #x.set_auto_chartostring( True )

	      atts = dict()
	      #x.setncattr( 'testatt', 'mytest' )
	      for vattname in variable.ncattrs() :
	         #x.setncattr( vattname, maybe_encode( variable.getncattr( vattname ) ) )
		 att = maybe_encode( variable.getncattr( vattname ) )
#                 print ('vattname: ', vattname , att )
#	         x.setncattr( vattname,att )
		 atts[ vattname ] = att

              x.setncatts( atts )
              outnc.variables[name][:] = self.nc_fid.variables[name][:]

	atts = dict()
	for name in self.nc_fid.ncattrs():
            att = self.nc_fid.getncattr( name )
	    atts[ name ] = maybe_encode( att )
	    #outnc.setncattr( name,  self.nc_fid.getncattr( name ) )
        outnc.setncatts( atts )

        outnc.close()

      def thinToVariableLand(self, varname, outncfilename ):

        outnc = netCDF4.Dataset( outncfilename, "w", format=self.nc_fid.data_model )

        for name, dimension in self.nc_fid.dimensions.iteritems():
	  outnc.createDimension(name, len(dimension) \
			  if not dimension.isunlimited() else None)

	for name, variable in self.nc_fid.variables.iteritems():
	    # take out the variable you don't want
	    if name == varname or name == "time" or name == "x" or name == "y" \
			    or name == "reference_time" or \
			    name == "ProjectionCoordinateSystem" : 
              x = outnc.createVariable( name, variable.datatype, \
			    variable.dimensions, zlib = True, complevel = 2)

	      for vattname in variable.ncattrs() :
	         x.setncattr( vattname, maybe_encode( variable.getncattr( vattname ) ) )

              outnc.variables[name][:] = self.nc_fid.variables[name][:]

	for name in self.nc_fid.ncattrs():
	    outnc.setncattr( name,  maybe_encode( elf.nc_fid.getncattr( name ) ) )

        outnc.close()

      def thinToVariableChannel(self, varname, outncfilename ):

        outnc = netCDF4.Dataset( outncfilename, "w", format=self.nc_fid.data_model )

        for name, dimension in self.nc_fid.dimensions.iteritems():
	  outnc.createDimension(name, len(dimension) \
			  if not dimension.isunlimited() else None)

	for name, variable in self.nc_fid.variables.iteritems():
	    # take out the variable you don't want
	    if name == varname or name == "time" or name == "feature_id" \
			    or name == "reference_time": 
              x = outnc.createVariable( name, variable.datatype, \
			    variable.dimensions, zlib = True, complevel = 2)

	      for vattname in variable.ncattrs() :
	         x.setncattr( vattname, maybe_encode( variable.getncattr( vattname ) ) )

              outnc.variables[name][:] = self.nc_fid.variables[name][:]

	for name in self.nc_fid.ncattrs():
	    outnc.setncattr( name,  maybe_encode( self.nc_fid.getncattr( name ) ) )

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
      
#     chn_and_land_files = [ f for f in os.listdir( nwmdir ) \
#		   if re.match( \
#	   r'nwm.t[0-9]{2}z\..*(channel_rt|land)(_[0-9])?\.(tm0[0-2]|f[0-9]{3})\.conus.nc(.gz)?',\
#                    f ) ]

#     for file in chn_and_land_files:
#       print "create_outputdir_and_get_list_of_files:", file
#       allfiles.append( '/nwm.' + datetimetag + '/' + case +'/' + file )

#     land_files = [ f for f in os.listdir( nwmdir ) \
#		   if re.match( \
#	   r'nwm.t[0-9]{2}z\..*land(_[0-9])?\.(tm0[0-2]|f[0-9]{3})\.conus.nc(.gz)?',\
#                    f ) ]
#
#     for file in land_files:
#       print "create_outputdir_and_get_list_of_files:", file
#       allfiles.append( '/nwm.' + datetimetag + '/' + case +'/' + file )

#     chn_files = [ f for f in os.listdir( nwmdir ) \
#		   if re.match( \
#	   r'nwm.t[0-9]{2}z\..*channel_rt(_[0-9])?\.(tm0[0-2]|f[0-9]{3})\.conus.nc(.gz)?',\
#                    f ) ]
#
#     for file in chn_files:
#       print "create_outputdir_and_get_list_of_files:", file
#       allfiles.append( '/nwm.' + datetimetag + '/' + case +'/' + file )

     forcing_files = [ f for f in os.listdir( nwmdir ) \
		   if re.match( \
	   r'nwm.t[0-9]{2}z\..*\.forcing\.(tm0[0-2]|f[0-9]{3})\.conus.nc(.gz)?',\
                    f ) ]

     for file in forcing_files:
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

def thin_files( infile, outfile, vars ):
       if infile.endswith( '.gz' ):
          inF = gzip.open( infile, 'rb' )
	  outF = open( outfile, 'wb' )
          file_content = inF.read()
          inF.close()
          outF.write( file_content )
          outF.close()
	  prod = WRFHydroModelProduct(  outfile[:-3] )
	  print 'thin: ', outfile[:-3]
          prod.thinToVariables( vars, outfile[:-6] + '.thinned.nc' )
	  os.remove( outfile[:-3] )
       else:
          prod = WRFHydroModelProduct(  infile )
	  print 'thin: ', outfile[:-3]
          prod.thinToVariables( vars, outfile[:-3] + '.thinned.nc' )


if __name__ == "__main__":
   pgmopt = main(sys.argv[1:])

indir = pgmopt[0]
outdir = pgmopt[1]
startdate = pgmopt[2]
enddate = pgmopt[3]

#cases = ['analysis_assim', 'short_range', 'medium_range',\
#		'long_range_mem1', 'long_range_mem2',\
#		'long_range_mem3', 'long_range_mem4', \
#		'forcing_analysis_assim', \
#		'forcing_short_range', \
#		'forcing_medium_range', \
#		'forcing_long_range_mem1', \
#		'forcing_long_range_mem2', \
#		'forcing_long_range_mem3', \
#		'forcing_long_range_mem4' ]

cases = ['forcing_medium_range' ]
sd = datetime.strptime(startdate, "%Y%m%d")
ed = datetime.strptime(enddate, "%Y%m%d")

while sd <= ed:

   allfilestocheck = []
   dttag = datetime.strftime(sd, "%Y%m%d")

   allfilestocheck = \
	create_outputdir_and_get_list_of_files( indir, outdir, cases, dttag )


   for file in allfilestocheck:

      #shutil.copyfile( indir + file, outdir + file )

      if re.match( \
         r'.*/nwm.t[0-9]{2}z\.short_range\.land\.f[0-9]{3}\.conus.nc(.gz)?', file ) :
	 thin_files( indir + file, outdir + file,\
           [ "SOILSAT_TOP","time","reference_time",\
	   "x","y","ProjectionCoordinateSystem"] )
			 
      elif re.match( \
         r'.*/nwm.t[0-9]{2}z\.(medium_range|long_range)\.land(_[0-9])?\.f[0-9]{3}\.conus.nc(.gz)?', file ) :
	 thin_files( indir + file, outdir + file,\
             [ "SNEQV", "SOILSAT_TOP","time","reference_time",\
	     "x","y","ProjectionCoordinateSystem"])
      elif re.match( \
         r'.*/nwm.t[0-9]{2}z\..*\.land\.tm0[012]\.conus.nc(.gz)?', file ) :
	 thin_files( indir + file, outdir + file,\
             [ "SOILSAT_TOP", "SNEQV", "SNOWH", "FSNO", "ACCET", "SNOWT_AVG", "nudge","time","reference_time","x","y","ProjectionCoordinateSystem"])
      elif re.match( \
         r'.*/nwm.t[0-9]{2}z\..*channel_rt(_[0-9])?\.f[0-9]{3}\.conus.nc(.gz)?', file ) :
	 thin_files( indir + file, outdir + file,\
           ['streamflow', 'feature_id','nudge','time','reference_time'])
      elif re.match( \
         r'.*/nwm.t[0-9]{2}z\..*channel_rt(_[0-9])?\.tm0[012]\.conus.nc(.gz)?', file ) :
	 thin_files( indir + file, outdir + file,\
           ['streamflow', 'nudge', 'feature_id','nudge',\
	   'time','reference_time'])
      elif re.match( \
         r'.*/nwm.t[0-9]{2}z\..*\.forcing\.(tm0[0-2]|f[0-9]{3})\.conus.nc(.gz)?', file ) :
	 thin_files( indir + file, outdir + file,\
           [ "RAINRATE", "T2D", "time","reference_time",\
	   "x","y","ProjectionCoordinateSystem"])
#	 thin_files( indir + file, outdir + file,\
#           [ "RAINRATE"])

   sd += timedelta( days = 1 )
