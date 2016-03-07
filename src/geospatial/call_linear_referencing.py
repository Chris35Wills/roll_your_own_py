"""
Takes in xy data and creates additional points using the linear_referencing 
function, creating points at a user set spacing (desired_spacing << units in m)

@author: Chris Williams
@date: 04/03/16
"""

import glob 
import Linear_referencing as lrf
import pyproj
import os

path="test_data/"
filenames=glob.glob("%s/*path*.csv" %(path))
projection = pyproj.Proj("+proj=stere +lat_0=90 +lat_ts=71 +lon_0=-39 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs")

for i in range(len(filenames)):
    print("Densifying %s" %(os.path.basename(filenames[i])))

    lrf.densify(filenames[i], \
        desired_spacing=200., \
        projection=projection, \
        xy_cols=[3,4], \
        plotting=False \
        )