import math
import numpy
import random
import sys
import matplotlib.pyplot as plt

di = 3
dj = 5

pi = math.pi

alpha = math.radians(float(sys.argv[1]))#numpy.arrange(0.1, pi/2, (pi/2-0.1)/100) #math.radians(float(sys.argv[1]))
erro = float(sys.argv[2])

C1 = math.sin(alpha)
C2 = 1.0/math.tan(alpha)
C3 = di*C1/(2*dj) + (C2*(dj + erro*dj)**2 - (2*(di - erro*di)*(dj + erro*dj)/C1))
C4 = (3*erro**2 + 2*erro + 1)*di**2 - (di*C1/(2*dj))*C2*(dj + erro*dj)**2

print C1, C2, C3, C4

X = (di - erro*di)/((dj + erro*dj)*C1) - C2
Y = di/(dj*C1) - C2
Z = (di + erro*di)/((dj - erro*dj)*C1) - C2

print X, Y, Z
T = numpy.arange(0, 1, 1.0/1000)
pdf = []
cdf = [0]
num = numpy.random.uniform(di - di*erro, di + di*erro, 1000)
den = numpy.random.uniform(dj - dj*erro, dj + dj*erro, 1000)

quo = (num/den)/C1 - C2

print len(quo)
xhist = numpy.arange(0,1, 1.0/1000)
hist = numpy.histogram(quo,bins=xhist, density=False)

for t in T:
	if t <= X:
		pdf.append(0)
		cdf.append(0)
	elif t > X and t <= Y:
		parcel1 = (dj + erro*dj)**2
		parcel2 = ((di - erro*di)**2)/(((t+C2)**2)*C1**2)
		summ = parcel1 - parcel2
		result = di*C1/(2*dj)*summ
		pdf.append(result)
		
		parcel2 = ((di - erro*di)**2)/((t+C2)*C1**2)
		summ = parcel1 + parcel2
		result = (di*C1/(2*dj)*summ + C3)
		cdf.append(result)

	elif t > Y and t <=Z:
		parcel1 = ((di + erro*di)**2)/(((t+C2)**2)*C1**2)
		parcel2 = (dj - erro*dj)**2
		summ = parcel1 - parcel2
		result = di*C1/(2*dj)*summ
		pdf.append(result)

		parcel1 = ((di + erro*di)**2)/((t+C2)*C1**2)
		summ = parcel2+parcel1
		result = C4 - (di*C1/(2*dj)*summ + C3)
		cdf.append(result)
	elif t>Z:
		pdf.append(0)
		cdf.append(1)

print len(cdf)
cdf.pop()
fig, ax1 = plt.subplots()

if sys.argv[3]=="4":
	ax2 = ax1.twinx()
	ax1.plot(xhist[0:999],hist[0], color="red")
	ax1.tick_params(axis="y")#, labelcolor="red")
	#plt.plot(xhist,quo)
	ax2.plot(T,pdf, linewidth=3.0)

if sys.argv[3]=="3":
	ax2 = ax1.twinx()
	ax2.plot(T, pdf)
	ax1.plot(T, cdf)


plt.show()
