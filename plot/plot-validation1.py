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
	tau = 0
	expectedR = 0
	for m in range(1,slrc):
		collisions = 1
		for k in range(m-1):
			if ((2.0**k)*cwMin) <= cwMax:
				tau = 2.0/((2.0**k)*cwMin+1)
			else:
				tau = 2.0/(cwMax + 1)
			num = nNodes*tau*(1.0 -tau)**(nNodes-1)
			den = 1.0 - (1.0 -tau)**nNodes
			collisions = collisions*(1.0 - num/den)

		if ((2.0**m)*cwMin) <= cwMax:
			tau = 2.0/((2.0**(m-1))*cwMin+1)
		else:
			tau = 2.0/(cwMax +1)
		num = tau*(1-tau)**(nNodes-1)
		den = 1 - (1 - tau)**nNodes
		expectedR += nNodes*(num/den)*collisions*m

	r = int(math.ceil(expectedR))
	txTime = 0
	for i in range(r):
		txTime += ((2**i)*cwMin/2)*tSlot
		#txTime += 1.0/((2**i)*cwMin + 1)*tSlot

	#txTime += tDifs + (r)*(tSifs+tData) + ((r-1)*timeOut) + (tSifs+tAck)
	txTime += tDifs + (r+1)*(tSifs+tData+tAck)

	return txTime, r



if __name__=="__main__":
	#dir1 = '../07-12-17'
	#dir1 = '../08-12-17'
	#dir1 = '../12-12-17'
	dir1 = '../15-12-17'

	nNodes = [5, 10, 15, 20, 25]
	slrc = [4, 8, 16, 32]
	std = "7"
	runs = 50
	cwmin = "32"
	
	f, axarr = plt.subplots(2, 2)

	sep = "-"
	for s in slrc:
		print "===== slrc =",s,"======"
		pkt=[]
		pktBar = []
		temp = []
		container = []
		containerBar = []
		plot = []
		validation = []
		for n in nNodes:
			for r in range(1,runs):
				lineCounter=0
				filename = dir1+"/"+str(n)+sep+std+sep+str(s)+sep+str(r)+sep+cwmin

				f = open(filename)
				
				temp.append(1 - float(f.readline())/(n*(n-1)))
				plot.append(float(f.readline()))

			container.append(avgCalc(plot))
			containerBar.append(intervalCalc(plot,95))	

			pkt.append(avgCalc(temp))
			pktBar.append(intervalCalc(temp,95))

			time = 0
			r = 0
			txRate = 6
			cwMin = 7
			cwMax = 4095
			tAck =  40.6901 ### 32.0*8.0/txRate
			tSifs = 10
			tSlot = 9 
			tDifs = (2*tSlot) + tSifs
			timeOut = 75
			tData = 76.2939# us  ###60*8.0/txRate
			time, r = wifiModel(n, s, cwMin,cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
			totalTime = 0
			transient = 0
			a = 0

			print "r", r
			print "time", time, container[0]/(n*(n-1))/1e-6
			#if r <= 1 :
			totalTime += n*(n-2)*time

			for j in range(1,n-1):
				transient, a = wifiModel(j, s, cwMin,cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
				totalTime += transient
			'''else:
				rate = int(math.floor(s/r))
				print "Rate", rate
				for j in range(1,rate):
					print "j1", j
					transient, a = wifiModel(n, s, (2**(j*r))*cwMin,cwMax, tAck, 
								tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += n*transient
				for j in range(rate, n-2-rate):			
					print "j2", j
					transient, a = wifiModel(n, s,cwMax, cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += n*transient
				for j in range(1,n-1):
					transient, a = wifiModel(j, s,cwMax, cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData)
					totalTime += transient #'''
			validation.append(totalTime/1e6)

			
		if s == 4:
			#plt.subplot(4,1,1)
			axarr[0,0].errorbar(nNodes,container, yerr=containerBar, c='blue', fmt='o')
			axarr[0,0].plot(nNodes,container, c='blue', ls='--', label='Simulation')
			axarr[0,0].plot(nNodes, validation, c = 'blue', label='Analysis')
			axarr[0,0].legend(loc=0)
			axarr[0,0].set_ylabel("Tempo (S)")
			axarr[0,0].set_xticks(nNodes)
			axarr[0,0].set_ylim(0,1)
			axarr[0,0].set_title("SLRC = "+str(s))

		elif s == 8:
			#plt.subplot(4,2,1)
			axarr[0,1].errorbar(nNodes,container, yerr=containerBar, c='green', fmt='o')
			axarr[0,1].plot(nNodes,container, c='green',ls='--', label='Simulation')
			axarr[0,1].plot(nNodes, validation, c = 'green', label='Analysis')
			axarr[0,1].legend(loc=0)
			axarr[0,1].set_ylabel("Tempo (S)")
			axarr[0,1].set_xticks(nNodes)
			axarr[0,1].set_ylim(0,1)
			axarr[0,1].set_title("SLRC = "+str(s))
			box = axarr[0,1].get_position()
			axarr[0,1].set_position([box.x0+0.1*box.width,box.y0,box.width, box.height ])

		elif s == 16:
			#plt.subplot(4,4,1)
			axarr[1,0].errorbar(nNodes,container, yerr=containerBar, c='red', fmt='o')
			axarr[1,0].plot(nNodes,container, c='red',ls='--', label='Simulation')
			axarr[1,0].plot(nNodes, validation, c = 'red', label='Analysis')
			axarr[1,0].legend(loc=0)
			axarr[1,0].set_ylabel("Tempo (S)")
			axarr[1,0].set_xticks(nNodes)
			axarr[1,0].set_ylim(0,1)
			axarr[1,0].set_title("SLRC = "+str(s))

		elif s == 32:
			#plt.subplot(4,4,2)
			axarr[1,1].errorbar(nNodes,container, yerr=containerBar, c='black', fmt='o')
			axarr[1,1].plot(nNodes,container, c='black', ls='--',label='Simulation')
			axarr[1,1].plot(nNodes, validation, c = 'black', label='Analysis')
			axarr[1,1].legend(loc=0)
			axarr[1,1].set_ylabel("Tempo (S)")
			axarr[1,1].set_xticks(nNodes)
			axarr[1,1].set_ylim(0,1)
			axarr[1,1].set_title("SLRC = "+str(s))
			box = axarr[1,1].get_position()
			axarr[1,1].set_position([box.x0+0.1*box.width,box.y0,box.width, box.height ])

	plt.suptitle("Simulation x Analysis \n CWMAX=65546    CWMIN=32")
	plt.legend(loc=0)
	plt.show()
