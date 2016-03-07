#!/usr/bin/python

###########################
# Program: Linear_referencing_FUNCTION.py
###########################

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys
import time
import pyproj

import ast

# Predefined projections
wgs84 = pyproj.Proj("+init=EPSG:4326")
utm22n = pyproj.Proj("+init=EPSG:32622")
bamber_npstereo = pyproj.Proj("+proj=stere +lat_0=90 +lat_ts=71 +lon_0=-39 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs")

#infile="C:/GitHub/synthetic_channels/test_output/site_6_PATHS/path_5.csv"
def densify(infile, desired_spacing=200., projection=pyproj.Proj("+init=EPSG:4326"), out_dir='', xy_cols=[3,4], plotting=True, save=True):
	"""
	Takes in a set of xy points (make sure they are sorted) and, treating the points as a continuous path, 
	adds additional points between them to achieve a more desirable point spacing.
	
	INPUTS:
	
	
	OUTPUTS:
	
	
	Example of function call: call_linear_referencing.py

	Modifed from A.Tedstone
	This version: Chris Williams
	@date: 03/03/16
	"""
	# Make some variables
	transect_sites = {}
	all_utmx = []
	all_utmy = []
	dist_positions = [-1]
	gps_distances = []
	tot_dist=0

	#open data
	site_coords = pd.read_csv(infile,sep=",", encoding="utf-8-sig") 

	xx=site_coords.iloc[:,xy_cols[0]]
	yy=site_coords.iloc[:,xy_cols[1]]
	coords=np.vstack([xx, yy]).transpose()[::-1]
	
	if plotting:
		# Iteritively plot coordinates
		# to check if points are sorted
		import time
		plt.axis([xx.min()-3000, xx.max()+3000, yy.min()-3000, yy.max()+3000])
		plt.ion()
		plt.title("Are input xy points sorted?\n %s" %(os.path.basename(infile)))
		plt.show()

		for i in range(len(coords)):
			point="%i" %i
			plt.scatter(coords[i,0],coords[i,1],label=point)
			plt.draw()
			time.sleep(0.05)
		
	if projection.is_latlong():
		print("converting to gridded xy")
		ux,uy = pyproj.transform(wgs84, gridded_prj, coords[:,0].values,coords[:,1].values)
		#plt.scatter(ux,uy), plt.title("input xy converted to gridded projection"), plt.show()
	else:
		ux,uy = xx,yy
		#plt.scatter(ux,uy), plt.title("input xy points"), plt.show()

	# Create additional points according to existing point spacing
	# and user set desired sample spacing
	transects=[None]*len(ux)
	
	for i in range(len(ux)-1):

		a = np.array((ux[i],uy[i]))
		b = np.array((ux[i+1],uy[i+1]))
		transects[i] = np.linalg.norm(b-a)

		# Use this to work out the sampling points based on requested sample spacing
		# First calculate remainder left over after regular spacing
		rem = transects[i] % desired_spacing
		n_points = (transects[i]-rem) / desired_spacing

		# Calculate end coordinates accounting for sample spacing
		# x = x1 + (lambda/distance) * (x2 - x1) [Donald's eqn]
		x_end_at = a[0] + ((transects[i]-rem)/transects[i]) * (b[0]-a[0])
		y_end_at = a[1] + ((transects[i]-rem)/transects[i]) * (b[1]-a[1])

		# Now define sampling locations in UTM
		if a[0] < x_end_at:
			utmx = np.linspace(a[0],x_end_at,num=n_points) 
		else:
			utmx = np.linspace(x_end_at,a[0],num=n_points) 
			utmx = utmx[::-1] #reverse
		if a[1] < y_end_at:
			utmy = np.linspace(a[1],y_end_at,num=n_points)
		else:
			utmy = np.linspace(y_end_at,a[1],num=n_points)
			utmy = utmy[::-1] #reverse

		for val in range(len(utmx)):
			all_utmx.append(utmx[val])
			all_utmy.append(utmy[val])

		# Save distance positions
		dph = np.arange(tot_dist,(tot_dist + (n_points * desired_spacing)),desired_spacing).tolist()
		dist_positions.extend(dph)

		# Save the transect distances at which the GPS sites are located
		gps_distances.append(tot_dist)

		# Increment total distance to include this transect
		tot_dist += transects[i]

	all_points=np.vstack([all_utmx, all_utmy]).transpose()
	
	if plotting:
		plt.clf()
		plt.plot(all_utmx, all_utmy, 'bo', label='new points')
		plt.plot(ux, uy, 'r*', label='original points')
		plt.title("New and old points\n %s" %(os.path.basename(infile)))
		plt.legend()
		plt.show()
		
	#convert output back to original projection....

	#save output
	if not out_dir:
		out_dir=os.path.dirname(infile)

	outfile=("%s/densified_%s.csv" %(out_dir,os.path.splitext(os.path.basename(infile))[0]))

	f=open(outfile, 'w')
	for i in range(len(all_points)):
		f.write("%f,%f\n" %(all_points[i,0],all_points[i,1]))
		print("%f,%f\n" %(all_points[i,0],all_points[i,1]))
		#print(all_points[i,:])

	f.close()

	return

if __name__  == "__main__":
	
	print("Functions to manipulate points along a line.")
	print("See available functions:")

	def top_level_functions(body):
	    return (f for f in body if isinstance(f, ast.FunctionDef))

	def parse_ast(filename):
	    with open(filename, "rt") as file:
	        return ast.parse(file.read(), filename=filename)

	#Printing functions in module...
	#http://stackoverflow.com/questions/139180/listing-all-functions-in-a-python-module
	filename="Linear_referencing_FUNCTION.py"
	tree = parse_ast(filename)
	for func in top_level_functions(tree.body):
		print("  %s" % func.name)