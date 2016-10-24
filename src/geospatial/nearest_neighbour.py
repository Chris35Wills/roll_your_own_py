import numpy as np
import matplotlib.pyplot as plt
import scipy.spatial

def get_nn(xy_1, xy_2, nn=1, radius=100):
	"""
	xy_1 and xy_2 must be 2xn arrays e.g. from 2 1d arrays use: xy = np.vstack((x1, y1)).T

	The kd tree will be made from xy_1
	The tree is then queried using xy_2
	Gets the nn nearest neighbour i.e. if nn = 1, the first nearest neighbour

	VARIABLES

		xy_1 		xy positions to be used to create kdtree

		xy_2 		xy positions used to query tree made from xy_1

		nn 		which neighbour to return

		radius 		search radius in units of xy coordinates of xy_1 and xy_2

	RETURNS

		indxs 		of length xy_2 (i.e. a value for every position in xy2) and each value 
				represents the nn neighbour xy in xy_1 to the given index position of xy_2

		dists 		of length xy_2 (i.e. a value for every position in xy2) and each value 
				represents the distance of the nn neighbour xy in xy_1 to the given index 
				position of xy_2 - if no nearest neighbour is found within the radius distance, 
				this will return as inf

	"""
	tree = scipy.spatial.KDTree(xy_1, leafsize=100)
	dists, indxs = tree.query(xy_2, k=nn, distance_upper_bound=radius)

	return dists, indxs

if __name__ is "__main__":

	# random data
	x1,y1,z1=[np.random.random_integers(0,100,100),np.random.random_integers(0,100,100),np.random.random_integers(0,10,100)]
	x2,y2,z2=[np.random.random_integers(0,100,100),np.random.random_integers(0,100,100),np.random.random_integers(0,10,100)]
	plt.plot(x1,y1,'r.')
	plt.plot(x2,y2,'b.')
	#plt.show()

	# create 2d data structure
	elev_xy = np.vstack((x1, y1)).T
	thick_xy = np.vstack((x2, y2)).T

	# kdtree
	radius=100.

	dists,indxs = get_nn(elev_xy, thick_xy, nn=1, radius=50)

	pos=1
	
	print("This is a test\n")

	print("The closest elev point to thick xy position %i (xy: %.1f,%.1f) is (xy: %.1f,%.1f) at a distance of %.1f" %(pos, thick_xy[pos][0], thick_xy[pos][1], elev_xy[indxs[pos]][0], elev_xy[indxs[pos]][1], dists[0]))




