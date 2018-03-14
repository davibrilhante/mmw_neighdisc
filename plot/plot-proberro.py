import math
import random
import numpy
import sys
import matplotlib.pyplot as plt

pi = math.pi

alpha = numpy.arange(0.1,pi/2, (pi/2-0.1)/100 )
#print len(alpha)
dj = 5.0
di = 3.0
erro = float(sys.argv[1])

nBeams = [4, 8, 16, 32]

for nb in nBeams:
	plotter = []
	for x in alpha:
		c1 = math.sin(x)
		c2 = 1.0/math.tan(x)
		k = (di*c1)/(2*dj)
		c3 = k*((c2*(di + erro*di)**2) - 2*((di - erro*di)*(dj + erro*dj))/c1)
		c4 = (di**2)*(1 + 3*erro**2 + 2*erro) - k*(c2*(dj - erro*dj)**2)

		theta = 1.0/math.tan((2*pi)/nb)
		print math.degrees((2*pi)/nb), math.degrees(x)		
		A = (di - erro*di)/((dj + erro*dj)*c1) - c2
		B = di/(dj*c1) - c2
		C = (di + erro*di)/((dj - erro*dj)*c1) - c2
		if theta <= A :
			plotter.append(1)

		elif theta > A and theta <= B:
			print 1
			pt1 = (dj + erro*dj)**2
			pt2 = ((di - erro*di)**2)/(c1**2)
			pt3 = 1.0/(theta+c2)
			prob = 1 - k*(pt1*theta + pt2*pt3) - c3
			plotter.append(prob)

		elif theta > B and theta <= C:
			print 2
			pt1 = (dj - erro*dj)**2
                        pt2 = ((di + erro*di)**2)/c1**2
                        pt3 = 1.0/(theta+c2)					
			prob = 1 - c4 + k*(pt1*theta + pt2*pt3)
			plotter.append(prob)

		elif theta > C:
			plotter.append(0)

	plt.plot(alpha, plotter)
	#print plotter
plt.show()
