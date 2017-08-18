import numpy
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab


di=5.0
dj=3.0


k1 = 0.1
k2 = 0.1

easy = True#False
samples = 300


if easy == False:
	Di = numpy.random.uniform(di-(k1*di),di+(k1*di),70000)#0.1,2*di,70000)#di-(k1*di),di+(k1*di),70000)
	Dj = numpy.random.uniform(dj-(k2*dj),dj+(k2*dj),70000)#0.1,2*dj,70000)#dj-(k2*dj),dj+(k2*dj),70000)
	n, bins, patches = plt.hist(Di/Dj, (samples/6.0), normed=True, facecolor='blue', alpha=0.75, label='Samples')
	plt.xlim(0,3) #b/d)
else:
	Di = numpy.random.uniform(0.1,2*di,70000)
	Dj = numpy.random.uniform(0.1,2*dj,70000)
	n, bins, patches = plt.hist(Di/Dj, (samples*3.0), normed=True, facecolor='blue', alpha=0.75, label='Samples')
	plt.xlim(0,6) #b/d)
	plt.ylim(0,1)

'''
plt.subplot(311)
n, bins, patches = plt.hist(Di, samples, normed=True, facecolor='green', alpha=0.75)
plt.plot(bins, numpy.ones_like(bins)/(2*di), linewidth=1, color='r')
plt.axis([0,10, 0, 3])

plt.subplot(312)
n, bins, patches = plt.hist(Dj, samples, normed=True, facecolor='green', alpha=0.75)
plt.plot(bins, numpy.ones_like(bins)/(2*dj), linewidth=1, color='r')
plt.axis([0,10,0,3])

plt.subplot(313)'''
#plt.xlim(0,20)
a = (di-(k1*di))
c = (dj+(k2*dj))
b = (di+(k1*di))
d = (dj-(k2*dj))

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
	q = [0]
        passo = ((b/d)+1)/samples

        #den = 4*k1*k2*di*dj
        #num = abs((a**2)-(di**2))
        #num = k1*di
	const1 = 1.0/(4*k1*k2)
	print const1
        fQ = [0]

        print passo, q, fQ, di/dj

        for i in range(1,samples+1):
                q.append(q[i-1] + passo)
                if q[i] <= (a/c): fQ.append(0)

		elif q[i]>(a/c) and q[i]<=(di/dj):
			fQ.append((dj/(2*di))*((c**2)-(a/q[i])**2))

		elif q[i]>(di/dj) and q[i]<=(b/d):
			fQ.append((dj/(2*di))*(((b/q[i])**2)-(d)**2))

                else: fQ.append(0)
                        #num = abs((di**2)-(b**2))
                        #fQ.append((num/den)*(1/(2*q[i]**2)))
	
print len(bins), len(fQ)
plt.plot(q, fQ, linewidth=3, color='r', label='PDF')
plt.title('Quociente de distribuicoes uniformes\n$d_i=$ '+str(di)+' e $d_j=$ '+str(dj))
print q.pop()		
#h, bins  = numpy.histogram(Di/Dj, bins=100, normed=True)
plt.legend(loc=1)
#bin_centers = (bins[1:]+bins[:-1])*0.5
#plt.plot(bin_centers, h )
#plt.axis([(dj-(k2*dj))*(di-(k1*di)),(di+(k1*di))*(dj+(k2*dj)),0,1])
#plt.xlim((dj-(k2*dj))*(di-(k1*di)),(di+(k1*di))*(dj+(k2*dj)))

plt.show()
