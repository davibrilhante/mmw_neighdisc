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


if __name__=="__main__":
	#dir1 = "../output-sector-norelief-11-44-44-09-12-17" #'../output-sector-norelief-09-23-08-07-12-17'
	dir1 = "/home/davi/outputs/17-16-01-04-02-18/" #13-02-13-29-01-18/"

	nNodes = [15, 30, 45, 60] #[20, 40, 60]#[5, 10, 15, 20, 25]
	nBeams = [8, 16, 32]
	meand = "2"
	meana = "2"
	relief = ["0","1"]
	runs = 30

        '''font = {'family' : 'normal',
        'size'   : 19}

        plt.rc('font', **font)'''

	oh_mdnd = []
	bf_mdnd = []
	ctrl_mdnd = []
	oh_cluster = []
	
	bf_cluster = []
	ctrl_cluster = []
	map_cluster = []
	
	erroh_mdnd = []
	errbf_mdnd = []
	errctrl_mdnd = []
	erroh_cluster = []
	errbf_cluster = []
	errctrl_cluster = []
	errmap_cluster = []


	container =[[],[],[],[],[],[],[]]

	print relief[0]
	
	sep = "-"
	#for n in nBeams:
	for n in nNodes:
		plot = []
		errorBars = []
		for r in range(1,runs):
			lineCounter=0
			filename = dir1+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+str(r)

			f = open(filename)
			#line = []
			while lineCounter < 7:
				if lineCounter == 0 or lineCounter == 3:
					container[lineCounter].append(float(f.readline())/((nNodes[1]-1)*(nNodes[1]-2)))
				else:
					container[lineCounter].append(float(f.readline()))
					
				lineCounter += 1
			#print line
			f.close()
			'''filename = dir1+sep+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+relief[1]+"/"+str(r)
			f = open(filename)
			while lineCounter<6:
				if lineCounter==4:
                                        container[lineCounter].append(float(f.readline()))
				else:
                                        container[lineCounter].append(float(f.readline())/1e6)
				lineCounter += 1'''

		oh_mdnd.append(avgCalc(container[0]))
		bf_mdnd.append(avgCalc(container[1]))
		ctrl_mdnd.append(avgCalc(container[2]))
		oh_cluster.append(avgCalc(container[3]))
		bf_cluster.append(avgCalc(container[4]))
		ctrl_cluster.append(avgCalc(container[5]))
		map_cluster.append(avgCalc(container[6]))

		#reliefBar.append(intervalCalc(container[5],95))
		erroh_mdnd.append(intervalCalc(container[0],95))
		errbf_mdnd.append(intervalCalc(container[1],95))
		errctrl_mdnd.append(intervalCalc(container[2],95))
		erroh_cluster.append(intervalCalc(container[3],95))
		errbf_cluster.append(intervalCalc(container[4],95))
		errctrl_cluster.append(intervalCalc(container[5],95))
		errmap_cluster.append(intervalCalc(container[6],95))

	#fig, ax1 = plt.subplots()
	#ax2 = ax1.twinx()
	#width = 0.35
	width = 1.0 
	
	plt.xticks(nNodes)
	
	#plt.subplot(2,1,1)
	for i in range(len(nNodes)): nNodes[i] -= width
	plt.bar(nNodes,oh_mdnd, width, color="b", label="mdnd", yerr=erroh_mdnd)
	for i in range(len(nNodes)): nNodes[i] += 2*width
	plt.bar(nNodes, oh_cluster, width, color="r", label="cluster", yerr=erroh_cluster)
	plt.legend(loc=0)

	
	'''
	#nNodes = [20, 40, 60]#[5, 10, 15, 20, 25]
	#plt.subplot(2,1,2)
	for i in range(len(nNodes)): nNodes[i] -= 2*width
	plt.bar(nNodes,bf_mdnd, width, color="c", label="bf_mdnd")
	for i in range(len(nNodes)): nNodes[i] += width
	plt.bar(nNodes, ctrl_mdnd, width, color="g", label="ctrl_mdnd")
	for i in range(len(nNodes)): nNodes[i] += 2*width
	plt.bar(nNodes, bf_cluster, width, color="y", label="bf_cluster")
	for i in range(len(nNodes)): nNodes[i] += width
	plt.bar(nNodes, ctrl_cluster, width, color="m", label="ctrl_cluster")
	for i in range(len(nNodes)): nNodes[i] += width
	plt.bar(nNodes, map_cluster, width, color="k", label="map_cluster")
	'''
	plt.ylabel("Tempo (S)")
	plt.ylabel("Tempo (S)")
	plt.xlabel("Numero de Nos")
	plt.xlabel("N"+u"ú"+"mero de N"+u"ó"+"s")

	plt.legend(loc=0, ncol=2)
	plt.show()
