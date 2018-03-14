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
	dir1 = "../output/25-01-18/"

	nNodes = [20, 40, 60]#[5, 10, 15, 20, 25]
	nBeams = [8, 16, 32]
	meand = "2"
	meana = "2"
	relief = ["0","1"]
	runs = 30

        font = {'family' : 'normal',
        'size'   : 19}

        plt.rc('font', **font)

	erroCluster = []
	norm = []
	cluster = []
	erroNorm = []
	
	normBar = []
	clusterBar = []
	erroNormBar = []
	erroClusterBar = []

	#reliefP = []
	#reliefBar = []
	#reliefErro = []
	#reliefErroBar = []
	
	container =[[],[],[],[],[],[]]

	print relief[0]
	
	sep = "-"
	for n in nBeams:
	#for n in nNodes:
		plot = []
		errorBars = []
		for r in range(1,runs):
			lineCounter=0
			filename = dir1+str(nNodes[1])+sep+str(n)+sep+meand+sep+meana+sep+str(r)

			f = open(filename)
			#line = []
			while lineCounter < 4:
				if lineCounter == 0 or lineCounter == 2:
					container[lineCounter].append(float(f.readline()))
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

		erroNorm.append(avgCalc(container[0]))
		norm.append(avgCalc(container[1]))
		erroCluster.append(avgCalc(container[2]))
		cluster.append(avgCalc(container[3]))
		#reliefErro.append(avgCalc(container[4]))
		#reliefP.append(avgCalc(container[5]))

		erroNormBar.append(intervalCalc(container[0],90))	
		normBar.append(intervalCalc(container[1],90))
		erroClusterBar.append(intervalCalc(container[2],90))
		clusterBar.append(intervalCalc(container[3],90))
		#reliefErroBar.append(intervalCalc(container[4],95))	
		#reliefBar.append(intervalCalc(container[5],95))

	'''#plt.subplot(1,3,1)
	plt.errorbar(nNodes,erro, yerr=erroBar, c='blue', fmt='o')
	plt.plot(nNodes,erro, c='blue', label='Erros Adjacentes')

	plt.errorbar(nNodes,reliefErro, yerr=reliefErroBar, c='red', fmt='o')
	plt.plot(nNodes,reliefErro, c='red', label='Acertos Adjacentes')
	plt.ylabel("Taxa de acertos prim"+u'á'+"rios")
	plt.xticks(nNodes)
	plt.xlabel("N"+u"ú"+"mero de N"+u"ó"+"s")
	plt.ylim(0,1)
	plt.legend(loc=0)'''
	
	#plt.subplot(1,3,2)
	#plt.subplot(1,2,1)
	plt.errorbar(nBeams,norm, yerr=normBar, c='green', fmt='o')
	plt.plot(nBeams, norm, c='green', label='MuNDi MaPP')

	plt.errorbar(nBeams, cluster, yerr=clusterBar, c='black', fmt='o')
	plt.plot(nBeams, cluster, c='black', label='cluster')

	
	#plt.errorbar(nNodes, reliefP, yerr=reliefBar, c='purple', fmt='o')
	#plt.plot(nNodes, reliefP, c='purple', label='MaPP Relief')
	plt.xticks(nBeams)
	plt.ylabel("Tempo (S)")
	plt.xlabel("N"+u"ú"+"mero de N"+u"ó"+"s")
	#plt.xlabel("Numero de Nos")
	plt.legend(loc=0)

	'''#plt.subplot(1,2,2)
	plt.errorbar(nNodes,mundiMapp, yerr=mundiMappBar, c='green', fmt='o')
	plt.plot(nNodes, mundiMapp, c='green', label='MuNDi MaPP')

	plt.errorbar(nNodes, goMundi, yerr=goMundiBar, c='black', fmt='o')
	plt.plot(nNodes, goMundi, c='black', label='Go MuNDi')
	
	plt.errorbar(nNodes,mdnd, yerr=mdndBar, c='red', fmt='o')
	plt.plot(nNodes, mdnd, c='red', label='MDND')
	plt.ylabel("Tempo (S)")
	plt.xlabel("Numero de Nos")
	plt.xlabel("N"+u"ú"+"mero de N"+u"ó"+"s")
	plt.xticks(nNodes)'''

	plt.legend(loc=0)
	plt.show()
