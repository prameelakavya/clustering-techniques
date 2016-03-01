#!/usr/bin/python
from a  import *
import sys
import scipy.misc, scipy.io, scipy.optimize, scipy.cluster.vq, scipy.spatial
from numpy import *

from matplotlib import pyplot, cm, colors, lines, animation
from mpl_toolkits.mplot3d import Axes3D

from sklearn import svm, datasets, metrics
from pylab import imread, imshow, gray

# if __name__ == "__main__":

# 	A = [	[0,1,0,0,1,0],
# 			[1,0,1,0,1,0],
# 			[0,1,0,1,0,0],
# 			[0,0,1,0,1,1],
# 			[1,1,0,1,0,0],
# 			[0,0,0,1,0,0]	]
# 	vcount =6

def gaussianDistance( X, sigma = 1.0 ):
	"""
	Create an adjacency using gaussian distance as the neigborhood similarity measure
	"""

	m 			= shape( X )[0]

	adjacency 	= zeros((m, m)) # adjacency matrix
	
	for i in xrange( 0, m ):
		for j in xrange( 0, m ):
			if i >= j: # since it's symmetric, just assign the upper half the same time we assign the lower half
				continue 
			adjacency[j, i] = adjacency[i, j] = sum( (X[i] - X[j])**2 )

#	print len(adjacency)
	adjacency = exp( -adjacency / (2 * sigma ** 2) ) - identity( m )
#	print len(adjacency),'ddddddddddddddddddddddddddddddd'
	return adjacency

def degreeMatrix( adjacency ):
	"""
	Create a degree matrix which is actually sum of each columns of the adjacency matrix
	Later on, this 'vector' can be converted to diagonal matrix using numpy.diag() function
	"""
	# return adjacency.sum( axis=1 )
	length = shape(adjacency)[0]
	degreeMatrix = zeros((length, length))
	
	for i in xrange(length):
		rowsum = 0
		for j in xrange(length):
			rowsum = rowsum + adjacency[i][j]
		degreeMatrix[i][i] = rowsum
	# degreeMatrix = asarray(degreeMatrix)
	# degreeMatrix = array(degreeMatrix)
	return degreeMatrix

def main():
	no_of_samples = 6
	data=[]
	data = a
	#data.append( datasets.make_moons(n_samples=no_of_samples, noise=0.05)[0] )
	#data.append( datasets.make_circles(n_samples=no_of_samples, factor=0.5, noise=0.05)[0] )

	# number of clusters we expect
	K = 3

	# from dataset, create adjacency, degree, and laplacian matrix
	adjacency 	= gaussianDistance( data, sigma=0.1 )
	print "adjacency:", adjacency
	degree 		= degreeMatrix( adjacency )
	print "degree", degree
	L = degree - adjacency
	print "L:", L
	#print len(adjacency), len(degree)
		#"""check what is wrong with this part========================================"""
		# L 			= diag(degree) - adjacency
		# print L,"yeha"

		# # perform whitening on the Laplacian matrix
		# deg_05 	= diag( degree  ** -0.5 )
		# print degree
		# L 		= deg_05.dot( L ).dot( deg_05 )

		# use eig to obtain eigenvalues and eigenvectors
	#	"""does my code really replace it?==========================================="""
	eigenvalues, eigenvectors = linalg.eig( L )

	# Sort the eigenvalues ascending, the first K zero eigenvalues represent the connected components
	idx = eigenvalues.argsort()
	eigenvalues.sort()
	evecs = eigenvectors[:, idx]
	eigenvectors = evecs[:, 0:K]
	print "eigenvalues[0:K]:", eigenvalues[0:K]
	color_array = ['b', 'r', 'g', 'y']

	fig = pyplot.figure( figsize=(15, 5) )
	fig.canvas.set_window_title( 'Difference between K-means and Spectral Clusterings' )
	#print type(X),type(K)
		# First perform the normal K-means on the original dataset and plot it out
	centroids, labels = scipy.cluster.vq.kmeans2( data, K )
#	print len(labels),'sdfghhgfsd'
	data = c_[data, labels]	
	ax = fig.add_subplot( 131 )
#	print len(data)
	ax.set_title('K means clustering')
	for k in range( 0, K ):
			ax.scatter( data[data[:, 4]==k, 0], data[data[:, 4]==k, 1], c=color_array[k], marker='o')

		# Then we perform spectral clustering, i.e. K-means on eigenvectors
	centroids, labels = scipy.cluster.vq.kmeans2( eigenvectors, K )
	#print len(labels), len(data),'adfghjdgsfadfsgdfh'
#	print len(data), 'before'
	data = c_[data, labels]	
#	print len(data), "after"
	ax = fig.add_subplot( 132 )
#	print '##############\n',data[:,5]
	ax.set_title('Spectral clustering')
	for k in range( 0, K ):
		ax.scatter( data[data[:, 5]==k, 0], data[data[:, 5]==k, 1],  c=color_array[k], marker='o')

		# Plot out the eigenvectors too
	data = c_[eigenvectors, labels]
#	print data
#	print len(data),'concatenate'
	ax = fig.add_subplot(133)
	ax.set_title('K-eigenvectors')
	for k in range( 0, K ):
		ax.scatter( data[data[:, 3]==k, 0], data[data[:, 3]==k, 1], c=color_array[k], marker='o')

	pyplot.show()
if __name__ == '__main__':
	main()
