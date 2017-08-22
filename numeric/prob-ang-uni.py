import numpy
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

pi = numpy.pi

theta = numpy.random.uniform(0,pi/2,70000)
seno = []
cotan = []
f = []
for i in theta: 
	seno.append(1/numpy.sin(i))
	cotan.append(1/numpy.tan(i))
	f.append(1/numpy.sin(i) - 1/numpy.tan(i))
samples = 300

plt.subplot(311)
n, bins, patches = plt.hist(seno, samples, normed=True, facecolor='green', alpha=0.75)
plt.plot(bins, numpy.ones_like(bins), linewidth=1, color='r')
plt.axis([0,10, 0, 3])

plt.subplot(312)
n, bins, patches = plt.hist(cotan, samples, normed=True, facecolor='green', alpha=0.75)
plt.plot(bins, numpy.ones_like(bins), linewidth=1, color='r')
plt.axis([0,10,0,3])

plt.subplot(313)
n, bins, patches = plt.hist(f, samples, normed=True, facecolor='green', alpha=0.75)
#plt.xlim(0,20)
#plt.ylim(0,1)
'''
a = (di-(k1*di))
c = (dj+(k2*dj))
b = (di+(k1*di))
d = (dj-(k2*dj))
plt.xlim(0, b/d)
easy = False

if easy == True:
	q = [0]
	passo = 20.0/samples#((b/c) - (a/d))/samples

	den = 4*k1*k2*di*dj
	num = abs((a**2)-(di**2))
	#num = k1*di

	fQ = [dj/(2*di)]#(num/den)*(1/(2*q[0]**2))]

	print passo, q, fQ, di/dj

	for i in range(1,samples+1):
		q.append(q[i-1] + passo)
		if q[i] <= (di/dj):
			num = abs((a**2)-(di**2))
			fQ.append(dj/(2*di))#(num/den)*(1/(2*q[i]**2)))
		else:
			num = abs((di**2)-(b**2))
			fQ.append(di/(2*dj*q[i]**2))#(num/den)*(1/(2*q[i]**2)))

else:
	q = [a/c]
        passo = ((b/d) - (a/c))/samples

        den = 4*k1*k2*di*dj
        num = abs((a**2)-(di**2))
        #num = k1*di

        fQ = [(num/den)*(1/(2*q[0]**2))]

        print passo, q, fQ, di/dj

        for i in range(1,samples+1):
                q.append(q[i-1] + passo)
                if q[i] <= (di/dj):
                        num = abs((a**2)-(di**2))
                        fQ.append((num/den)*(1/(2*q[i]**2)))
                else:
                        num = abs((di**2)-(b**2))
                        fQ.append((num/den)*(1/(2*q[i]**2)))
	
		
print len(bins), len(fQ)
#plt.plot(q, fQ, linewidth=3, color='black')
plt.title('Quociente de distribuicoes uniformes\n$d_i=$ '+str(di)+' e $d_j=$ '+str(dj))
#h, bins  = numpy.histogram(Di/Dj, bins=100, normed=True)
#plt.plot(bins, numpy.ones_like(bins), linewidth=1, color='r')
#bin_centers = (bins[1:]+bins[:-1])*0.5
#plt.plot(bin_centers, h )
#plt.axis([(dj-(k2*dj))*(di-(k1*di)),(di+(k1*di))*(dj+(k2*dj)),0,1])
#plt.xlim((dj-(k2*dj))*(di-(k1*di)),(di+(k1*di))*(dj+(k2*dj)))
'''
plt.show()
