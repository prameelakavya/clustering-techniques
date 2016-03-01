from numpy import *
import ast
a=[]
txt = open('iris.dat')
for line in txt:
    line = line.split(',')
    a.append(line)
for i in a:
    i[-1] = i[-1].strip()
  #  print i
for i in a:
    if i[-1] == 'Iris-setosa':
	k=a.index(i)
	a[k][-1] = '1'
    elif i[-1] == 'Iris-versicolor':
	k=a.index(i)
	a[k][-1] = '2'
    elif i[-1] == 'Iris-virginica':
	k=a.index(i)
	a[k][-1] = '3'

for i in a:
    for j in i:
	k=a.index(i)
	l=i.index(j)
	a[k][l] = ast.literal_eval(j)
b=[]
for i in a:
	b.append(i[-1])
	i.pop()
#	print i
#print b
a = array(a)
#print type(a)
#print len(a), len(b)

