"""
Program: geotiff_tools.py 

Functions for dealing with geotiffs.

@ Chris Williams 15/01/16
"""

from __future__ import division

import sys
import numpy as np

from osgeo import gdal, osr
from osgeo.gdalconst import *
from osgeo import gdal, gdalconst

def resample_geotiff(src_filename, dst_filename, new_post=1000):
	'''
	Resamples an input DEM to a new post size.
	Pass in either source data filename or open array.
	Bilinear interpolation is used to populate the new grid.

	VARIABLES
	#src_filename = "C:/input.tif" 
	#dst_filename = "C:/output.tif" 
	#new_post=500

	HOW TO CALL
	resample_geotiff(src_filename, dst_filename, new_post)

	OUTPUT
	Saves a version of the resampled array to dst_filename 
	Returns a gdal dataset object of the new array + teh new array (as tuple)
	
	***ADDITIONS THAT COULD BE MADE***

	Overwrite option?
	Modify output directory catch?

	RETURNS 
	A gdal dataset object of the output tiff (see: http://www.gdal.org/classGDALDataset.html)
	'''	

	#Read in source dataset
	src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
	src_proj = src.GetProjection()
	src_geotrans = src.GetGeoTransform() # 1st [0] value is bl_x and 4th [3] value is tr_y
	cols = src.RasterXSize 
	rows = src.RasterYSize
	post = src_geotrans[1]

	#Corners
	tr_y = src.GetGeoTransform()[3]
	bl_x = src.GetGeoTransform()[0]
	bl_y = src.GetGeoTransform()[3]-(src.RasterYSize*src.GetGeoTransform()[1])
	tr_x = src.GetGeoTransform()[0]+(src.RasterXSize*src.GetGeoTransform()[1])

	#Create new geotransform 
	post_out=post/(post/new_post) ### <<< easy test!!! assert post_out == new_post
	new_rows = int(((rows-1)*(post/new_post))+1) # if rows = 1121, post = 2500, and new_post = 1000, new rows == 2801
	new_cols = int(((cols-1)*(post/new_post))+1) # if cols = 601, post = 2500, and new_post = 1000, new cols == 1501
	new_tl_y=bl_y + (rows*post)
	out_geotrans=(bl_x, post_out, 0.0, new_tl_y, 0.0, post_out*-1)

	#Define output file
	dst = gdal.GetDriverByName('GTiff').Create(dst_filename, int(new_cols), int(new_rows), 1, gdalconst.GDT_Float32)
	dst.SetGeoTransform(out_geotrans)
	dst.SetProjection(src_proj) # same as input

	#Reproject
	gdal.ReprojectImage(src, dst, src_proj, src_proj, gdalconst.GRA_Bilinear)

	#Flush
	del dst

	#Open resampled data
	resampled_dataset = gdal.Open(dst_filename, GA_ReadOnly)
	
	return resampled_dataset

if __name__ == '__main__':
	print("Wrappers for dealing with geotiffs in different ways")
