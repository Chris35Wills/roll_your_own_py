import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

"""
Quick plotting wrappers using matplotlib
"""

def plot(array, title='', cbar=False):
	"""
	Simple 2D surface plot - just shows an image

	VARIABLES
		array - A simple 2D array of values

	RETURNS
		Nothing
	"""
	plt.imshow(array)
	if cbar != False: plt.colorbar()
	if title != '': plt.title(title)
	plt.show()

def plot_3d_surface(array, title=''):
	"""
	Simple 3D surface plot - takes in a 2D array, creates a meshgrid and displays it in 3D

	VARIABLES
		array - A simple 2D array of values

	RETURNS
		Nothing
	"""
	ny,nx=array.shape
	x = np.linspace(0, 1, nx)
	y = np.linspace(0, 1, ny)
	xv, yv = np.meshgrid(x, y)

	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.plot_surface(xv, yv, array, cmap=cm.coolwarm)
	if title != '': plt.title(title)
	plt.show()
