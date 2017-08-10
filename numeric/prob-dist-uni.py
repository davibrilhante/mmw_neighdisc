import numpy
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


di=5
dj=3


k1 = 0.1
k2 = 0.1

Di = numpy.random.uniform(0.1,2*di,70000)#di-(k1*di),di+(k1*di),70000)
Dj = numpy.random.uniform(0.1,2*dj,70000)#dj-(k2*dj),dj+(k2*dj),70000)

samples = 300

plt.subplot(311)
n, bins, patches = plt.hist(Di, samples, normed=True, facecolor='green', alpha=0.75)
plt.plot(bins, numpy.ones_like(bins)/(2*k1*di), linewidth=1, color='r')
plt.axis([0,10, 0, 3])

plt.subplot(312)
n, bins, patches = plt.hist(Dj, samples, normed=True, facecolor='green', alpha=0.75)
plt.plot(bins, numpy.ones_like(bins)/(2*k2*dj), linewidth=1, color='r')
plt.axis([0,10,0,3])

plt.subplot(313)
n, bins, patches = plt.hist(Di/Dj, samples, normed=True, facecolor='green', alpha=0.75)
a = (di-(k1*di))
c = (dj+(k2*dj))
b = (di+(k1*di))
d = (dj-(k2*dj))

q = [a/d]
passo = ((b/c) - (a/d))/samples

den = 4*k1*k2*di*dj
num = abs((a**2)-(di**2))
#num = k1*di

fQ = [(num/den)*(1/(2*q[0]**2))]

for i in range(1,samples+1):
	q.append(q[i-1] + passo)
	if q <= (di/dj):
		num = abs((a**2)-(di**2))
		fQ.append((num/den)*(1/(2*q[i]**2)))
	else:
		num = abs((di**2)-(b**2))
		fQ.append((num/den)*(1/(2*q[i]**2)))
		
		
print len(bins), len(fQ)
plt.plot(bins, fQ, linewidth=3, color='r')
#h, bins  = numpy.histogram(Di/Dj, bins=100, normed=True)
#plt.plot(bins, numpy.ones_like(bins), linewidth=1, color='r')
#bin_centers = (bins[1:]+bins[:-1])*0.5
#plt.plot(bin_centers, h )
#plt.axis([(dj-(k2*dj))*(di-(k1*di)),(di+(k1*di))*(dj+(k2*dj)),0,1])
#plt.xlim((dj-(k2*dj))*(di-(k1*di)),(di+(k1*di))*(dj+(k2*dj)))

plt.show()
