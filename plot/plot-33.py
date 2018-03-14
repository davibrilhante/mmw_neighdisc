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
	dir1 = "../output/sector"

	nNodes = [5, 10, 15, 20, 25]
	nBeams = [4, 8, 16, 32]
	meand = "2"
	meana = "2"
	relief = ["0","1"]
	runs = 200

	mdnd = []
	mundiMapp = []
	goMundi = []
	erro = []
	
	mdndBar = []
	mundiMappBar = []
	goMundiBar = []
	erroBar = []

	reliefP = []
	reliefBar = []
	reliefErro = []
	reliefErroBar = []
	
	container =[[],[],[],[],[],[]]

	print relief[0]

	font = {'family' : 'normal',
        'size'   : 19}

        plt.rc('font', **font)

	
	sep = "-"
	for n in nBeams:
	#for n in nNodes:
		plot = []
		errorBars = []
		for r in range(1,runs):
			lineCounter=0
			filename = dir1+sep+str(nNodes[2])+sep+str(n)+sep+meand+sep+meana+sep+relief[0]+"/"+str(r)

			f = open(filename)
			#line = []
			while lineCounter < 4:
				if lineCounter == 0:
					container[lineCounter].append(float(f.readline()))
				else:
					container[lineCounter].append(float(f.readline())/1e6)
					
				lineCounter += 1
			#print line
			f.close()
			filename = dir1+sep+str(nNodes[2])+sep+str(n)+sep+meand+sep+meana+sep+relief[1]+"/"+str(r)
			f = open(filename)
			while lineCounter<6:
				if lineCounter==4:
                                        container[lineCounter].append(float(f.readline()))
				else:
                                        container[lineCounter].append(float(f.readline())/1e6)
				lineCounter += 1

		erro.append(avgCalc(container[0]))
		mundiMapp.append(avgCalc(container[1]))
		goMundi.append(avgCalc(container[2]))
		mdnd.append(avgCalc(container[3]))
		reliefErro.append(avgCalc(container[4]))
		reliefP.append(avgCalc(container[5]))

		erroBar.append(intervalCalc(container[0],95))	
		mundiMappBar.append(intervalCalc(container[1],95))
		goMundiBar.append(intervalCalc(container[2],95))
		mdndBar.append(intervalCalc(container[3],95))
		reliefErroBar.append(intervalCalc(container[4],95))	
		reliefBar.append(intervalCalc(container[5],95))

	#plt.subplot(1,3,1)
	plt.errorbar(nBeams,erro, yerr=erroBar, c='blue', fmt='o')
	plt.plot(nBeams,erro, c='blue', label='Consider Adjacent Error')

	plt.errorbar(nBeams,reliefErro, yerr=reliefErroBar, c='red', fmt='o')
	plt.plot(nBeams,reliefErro, c='red', label='Not Consider Adjacent Error')
	#plt.ylabel("Taxa de acertos prim"+u"á"+"rios")
	plt.ylabel("Primary Matching Rate")
	plt.xticks(nBeams)
	#plt.xlabel("N"+u"ú"+"mero de Setores")
	plt.xlabel("Number of Sectors")
	plt.ylim(0,1)
	plt.legend(loc=0)
	'''
	#plt.subplot(1,3,2)
	#plt.subplot(1,2,1)
	plt.errorbar(nBeams,mundiMapp, yerr=mundiMappBar, c='green', fmt='o')
	plt.plot(nBeams, mundiMapp, c='green', label='MuNDi MaPP')

	plt.errorbar(nBeams, goMundi, yerr=goMundiBar, c='black', fmt='o')
	plt.plot(nBeams, goMundi, c='black', label='Go MuNDi')

	
	plt.errorbar(nBeams, reliefP, yerr=reliefBar, c='purple', fmt='o')
	plt.plot(nBeams, reliefP, c='purple', label='MaPP Relief')
	plt.xticks(nBeams)
	plt.ylabel("Time (S)")
	#plt.xlabel("Numero de Setores")
	plt.xlabel("Number of Sectors") 
	plt.ylim(0,1.5)
	plt.legend(loc=3)

	
	#plt.subplot(1,2,2)
	#plt.subplot(1,3,3)
	plt.errorbar(nBeams,mundiMapp, yerr=mundiMappBar, c='green', fmt='o')
	plt.plot(nBeams, mundiMapp, c='green', label='mundiMapp')

	plt.errorbar(nBeams, goMundi, yerr=goMundiBar, c='black', fmt='o')
	plt.plot(nBeams, goMundi, c='black', label='goMundi')
	
	plt.errorbar(nBeams,mdnd, yerr=mdndBar, c='red', fmt='o')
	plt.plot(nBeams, mdnd, c='red', label='MDND')
	plt.ylabel("Temp (S)")
	#plt.xlabel("Numero de Setores")
	plt.xlabel("N"+u"ú"+"mero de Setores")
	plt.ylim(0,15)
	plt.xticks(nBeams)'''

	#plt.suptitle("Numero de Nos: 15")
	plt.legend(loc=0)
	plt.show()
