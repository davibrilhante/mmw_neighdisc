# Using the magic encoding
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import sys
import math


def avgCalc(array):
        return sum(array)/len(array)

def intervalCalc(array,conf):
        dummy = 0
	mean = avgCalc(array)
        for i in array: dummy += (i - mean)**2
        stdDev = math.sqrt(dummy/len(array))

        barStart = mean - stdDev
        barEnd = mean +stdDev
        if conf == 90: z=1.645
        elif conf == 95: z=1.96
        elif conf == 98: z=2.326
        elif conf == 99: z=2.576
        else: "Confidence interval not specified.Try 90, 95, 98 or 99"
        return stdDev*z/math.sqrt(len(array))#, barStart, barEnd


def wifiModel(nNodes, slrc, cwMin,cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData):
	expectedR = 0
	for m in range(1,slrc):
		collisions = 1
		for k in range(1, m-1):
			if ((2.0**k)*cwMin) <= cwMax:
				tau = 2.0/((2.0**k)*cwMin+1)
			num = nNodes*tau*(1.0 -tau)**(nNodes-1)
			den = 1.0 - (1.0 -tau)**nNodes
			collisions = collisions*(1.0 - num/den)
		if ((2.0**m)*cwMin) <= cwMax:
			tau = 2.0/((2.0**m)*cwMin+1)
		num = tau*(1-tau)**(nNodes-1)
		den = 1 - (1 - tau)**nNodes

		expectedR += nNodes*(num/den)*collisions*m

	r = math.ceil(expectedR)
	txTime = 0
	for i in range(r):
		txTime += 1.0/((2**r)*cwMin + 1)

	txTime += tDifs + (r)*(tSifs+tData) + ((r-1)*timeOut) + (tSifs+tAck)

	return txTime, r



if __name__=="__main__":
	#dir1 = '../07-12-17'
	#dir1 = '../08-12-17'
	#dir1 = '../12-12-17'
	dir1 = '../16-12-17'

	nNodes = [5, 10, 15, 20, 25]
	cwmax = [1024, 4096, 16384, 65536]
	std = "7"
	runs = 50
	cwmin = "32"

        font = {'family' : 'normal',
        'size'   : 18}

        plt.rc('font', **font)

	sep = "-"
	for s in cwmax:
		pkt=[]
		pktBar = []
		temp = []
		container = []
		containerBar = []
		plot = []
		for n in nNodes:
			for r in range(1,runs):
				lineCounter=0
				#filename = dir1+"/"+str(n)+sep+std+sep+str(s)+sep+str(r)
				filename = dir1+"/"+str(n)+sep+std+sep+cwmin+sep+str(s)+sep+str(r)
				f = open(filename)
				
				temp.append(1 - float(f.readline())/(n*(n-1)))
				plot.append(float(f.readline()))

			container.append(avgCalc(plot))
			containerBar.append(intervalCalc(plot,95))	

			pkt.append(avgCalc(temp))
			pktBar.append(intervalCalc(temp,95))

		'''	time = 0
			r = 0
			txRate = 6
			cwMin = 7
			cwMax = 1024
			tAck =  32.0*8.0/txRate
			tSifs = 10
			tSlot = 9 
			tDifs = 2*tSlot + tSifs
			timeOut = 75
			tData = 60*8.0/txRate
			time, r = wifiModel(n, s, cwMin,cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
			totalTime = 0
			transient = 0
			a = 0

			if r <= 1 :
				totalTime += n*(n-1)*time

				for j in range(1,n-1):
					transient, a = wifiModel(n, s, cwMin,cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += transient
			else:
				rate = math.floor(s/r)
				for j in range(1,rate):
					transient, a = wifiModel(n, s, (2**(j*r))*cwMin,cwMax, tAck, 
								tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += n*transient
				for j in (rate, n):			
					transient, a = wifiModel(n, s,cwMax, cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += n*transient
				for j in range(1,n-1):
					transient, a = wifiModel(j, s,cwMax, cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += transient'''

			
		if s == 1024:
			'''plt.subplot(2,1,1)
			plt.errorbar(nNodes,container, yerr=containerBar, c='blue', fmt='o')
			plt.plot(nNodes,container, c='blue', label='cwmax='+str(s))
			plt.legend(loc=0)
			plt.ylabel("Tempo (S)")
			plt.xticks(nNodes)

			plt.subplot(2,1,2)'''
			plt.errorbar(nNodes,pkt, yerr=pktBar, c='blue', fmt='o')
			plt.plot(nNodes, pkt, c = 'blue', label='cwmax='+str(s))
			plt.ylabel("% de entrega")
			plt.ylim(0.900, 1.00)
			plt.xlabel("N"+u'ú'+"mero de N"+u'ó'+"s")
			plt.xticks(nNodes)

		'''elif s == 4096:
			plt.subplot(2,1,1)
			plt.errorbar(nNodes,container, yerr=containerBar, c='green', fmt='o')
			plt.plot(nNodes,container, c='green', label='cwmax='+str(s))
			plt.legend(loc=0)
			plt.ylabel("Tempo (S)")
			plt.xticks(nNodes)

			plt.subplot(2,1,2)
			plt.errorbar(nNodes,pkt, yerr=pktBar, c='green', fmt='o')
			plt.plot(nNodes, pkt, c = 'green', label='cwmax='+str(s))
			plt.xticks(nNodes)
			plt.ylabel("% de entrega")

		elif s == 16384:
			plt.subplot(2,1,1)
			plt.errorbar(nNodes,container, yerr=containerBar, c='red', fmt='o')
			plt.plot(nNodes,container, c='red', label='cwmax='+str(s))
			plt.legend(loc=0)
			plt.ylabel("Tempo (S)")
			plt.xticks(nNodes)

			plt.subplot(2,1,2)
			plt.errorbar(nNodes,pkt, yerr=pktBar, c='red', fmt='o')
			plt.plot(nNodes, pkt, c = 'red', label='cwmax='+str(s))
			plt.xticks(nNodes)
			plt.ylabel("% de entrega")

		elif s == 65536:
			plt.subplot(2,1,1)
			plt.errorbar(nNodes,container, yerr=containerBar, c='black', fmt='o')
			plt.plot(nNodes,container, c='black', label='cwmax='+str(s))
			plt.legend(loc=0)
			plt.ylabel("Tempo (S)")
			plt.xticks(nNodes)

			plt.subplot(2,1,2)
			plt.errorbar(nNodes,pkt, yerr=pktBar, c='black', fmt='o')
			plt.plot(nNodes, pkt, c = 'black', label='cwmax='+str(s))
			plt.xticks(nNodes)
			plt.ylabel("% de entrega")
			plt.xlabel("Numero de Nos")'''

	#plt.suptitle("CWMIN= "+str(cwmin))
	plt.legend(loc=0)
	plt.show()
