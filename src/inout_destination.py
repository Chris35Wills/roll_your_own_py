"""
Program: inout_destination.py 

Functions for checking existance of paths and files, creating them if required.

@ Chris Williams 15/01/16
"""

from __future__ import division

import os
import os.path
import numpy as np
import time as time

def check_output_dir(filename):
	'''
	Checks if the designated directory name exists, creating it if it doesn't

	INPUT
	filename = Complete path and filename of proposed output (e.g. 'C:/foo.txt')

	RETURNS
	nothing
	'''
	dirname = os.path.dirname(filename)
	if not os.path.isdir(dirname):	
		print "%s DOESN'T exist...\n" % dirname
		os.makedirs(dirname) 
		print "...but it does now"

def check_if_file_exists(filename):
	'''
	Checks an path/file string to see if the designated file exists.
	If file already exists, creates a time stamped version if it does

	INPUT
	filename = Complete path and filename of proposed output (e.g. 'C:/foo.txt')
	
	RETURNS
	filename (modified if already existing)
	'''

	if os.path.isfile(filename):	
		print "%s Already exists...\n" % filename
		zeit=time.strftime('%H''%M''%S')
		date=time.strftime('%d''%m''%y')

		dir_name=os.path.dirname(filename)
		basename=os.path.splitext(os.path.basename(filename))[0] 

		ofile="%s/%s_STAMP_%s_%s.tif" %(dir_name, basename, zeit, date)
		print("Renaming output with time and date stamp: %s" %(ofile))
		
		return ofile

	else:
		return filename


if __name__ = '__main__':
	print("Wrappers for checking if directories or files for output exist, creating them if necessary")

