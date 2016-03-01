import os
import sys
from math import *
import numpy as np

dataset = "iris.data"
mergedclusters = []

def getLines(dataset):
	with open(dataset, 'rb') as data:
		lines = data.read().splitlines()
		temp = []
		for i in lines:
			i = i.split(',')
			i.pop()
			for j in range(0,len(i)):
				i[j] = float(i[j])
			temp.append(i)
		lines = temp
	return lines

def euclidean_dist(a,b):
	l = len(a)
	sum = 0
	for i in range(0,l):
		sum += pow(a[i]-b[i],2)
	d = sqrt(sum)
	return d

def centroid(D):
	a = np.array(D)
	cent = a.mean(axis=0).tolist()
	return cent

def metric1(C1,C2):
	l1 = len(C1)
	l2 = len(C2)

	d = 10000
	for i in range(0,l1):
		for j in range(0,l2):
			dist = euclidean_dist(C1[i],C2[j])
			if dist < d:
				d = dist
	return d
def metric2(C1,C2):
	l1 = len(C1)
	l2 = len(C2)

	d = -10000
	for i in range(0,l1):
		for j in range(0,l2):
			dist = euclidean_dist(C1[i],C2[j])
			if dist > d:
				d = dist
	return d

def metric3(C1,C2):
	l1 = len(C1)
	l2 = len(C2)

	d = 0
	for i in range(0,l1):
		for j in range(0,l2):
			dist = euclidean_dist(C1[i],C2[j])
			d += dist
	d = d/(l1*l2)
	return d	

def metric4(C1,C2):
	cent1 = centroid(C1)
	cent2 = centroid(C2)

	return euclidean_dist(cent1,cent2)

def clustering(C):
	temp = C
	d = 100000
	for key,value in C.iteritems():
		for key1,value1 in temp.iteritems():
			dist = metric4(value,value1)
			if dist < d:
				d = dist
				if key < key1:
					k = key
					k1 = key1
				else:
					k = key1
					k1 = key
				a = value
				b = value1
	mergedclusters.append([(k,a),(k1,b),k])
	C[k] = C[k] + value1
	del C[k1]
	return C

def call_clustering(C):
	while len(C) > 1:
		C = clustering(C)
	return C			


def main():
	data = getLines(dataset)
	clusterId = {}
	clusters = {}
	l = len(data)
	
	for i in range(0,l):
		clusters[i] = []
		clusterId[i] = i
		clusters[i].append(data[i])
	C = call_clustering(clusters)
	print "agglomerative clustering done!"

if __name__ == '__main__':
	main()
