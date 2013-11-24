#!/usr/bin/python

import sys, getopt
import os

gzlist = []
tarlist = []

def main(argv):
   srcdir = ''
   dstdir = ''
   startdate = ' '
   sfr = ' '
   enddate = 0
   try:
      opts, args = getopt.getopt(argv,"h:i:o:s:e:r:",["idir=","odir=","s_date=","e_date=", "sfr="])
   except getopt.GetoptError:
        print 'ERROR restore.py -i <srcdir> -o <dstdir> -s <startdate> [-e <enddate>] [-r <dir>]'
        sys.exit(4)
   for opt, arg in opts:
      if opt == '-h':
         print 'restore.py -i <srcdir> -o <dstdir> -s <startdate> -e <enddate>'
         sys.exit()
      elif opt in ("-i", "--idir"):
         srcdir = arg
      elif opt in ("-o", "--odir"):
         dstdir = arg
      elif opt in ("-s", "--s_date"):
         startdate= arg
      elif opt in ("-e", "--e_date"):
         enddate = arg
      elif opt in ("-r", "--sfr"):
         sfr = arg
      else:
        print 'restore.py -i <srcdir> -o <dstdir> -s <startdate> -e <enddate>'

   print 'Input file is "', srcdir
   print 'Output file is "', dstdir
   print 'Start date is"', startdate
   print 'End date is "', enddate
   print ' SFR is "',sfr
   if not os.path.exists(srcdir):
        print 'Source Path Not Found'
        sys.exit(1)
   if not os.path.exists(dstdir):
        os.makedirs(dstdir)

   for files in os.listdir(srcdir):
        if files.endswith(".gz"):
                param, value = files.split("_", 1)
                if param >= str(startdate):
                        if enddate != 0 and param <= str(enddate):
                                gzlist.append(files)

   for file in gzlist:
        cmd = 'gzip -d ' + srcdir +'/' + file
        print cmd
        os.system(cmd)

   for files in os.listdir(srcdir):
        if files.endswith(".tar"):
                param, value = files.split("_", 1)
                if param >= str(startdate):
                        if enddate != 0 and param <= str(enddate):
                                tarlist.append(files)

   tarlist.sort()
   for file in tarlist:
        cmd = ' tar -xvf ' + srcdir+ '/' + file + ' -C ' + dstdir +' ' + sfr
        print cmd
        os.system(cmd)


if __name__ == "__main__":
   main(sys.argv[1:])
##########################################################################
                                                                              
