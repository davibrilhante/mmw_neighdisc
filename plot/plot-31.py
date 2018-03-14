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
	dir1 = "../output-sector-norelief-01-12-03-15-12-17"

	nNodes = [10, 15, 20, 25]
	nBeams = [4, 8, 16, 32]
	meand = "2"
	meana = "2"
	relief = "0"
	runs = 30

	mdnd = []
	mundiMapp = []
	goMundi = []
	erro = []
	
	mdndBar = []
	mundiMappBar = []
	goMundiBar = []
	erroBar = []

	container =[[],[],[],[]]
	sep = "-"
	#for n in nBeams:
	for n in nNodes:
		plot = []
		errorBars = []
		for r in range(1,runs):
			lineCounter=0
			filename = dir1+"/"+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+str(r)

			f = open(filename)
			#line = []
			while lineCounter < 4:
				if lineCounter == 0:
					container[lineCounter].append(float(f.readline()))
				else:
					container[lineCounter].append(float(f.readline())/1e6)
				lineCounter += 1
			#print line
		erro.append(avgCalc(container[0]))
		mundiMapp.append(avgCalc(container[1]))
		goMundi.append(avgCalc(container[2]))
		mdnd.append(avgCalc(container[3]))

		erroBar.append(intervalCalc(container[0],95))	
		mundiMappBar.append(intervalCalc(container[1],95))
		goMundiBar.append(intervalCalc(container[2],95))
		mdndBar.append(intervalCalc(container[3],95))

	plt.subplot(3,1,1)
	plt.errorbar(nBeams,erro, yerr=erroBar, c='blue', fmt='o')
	plt.plot(nBeams,erro, c='blue')
	plt.ylabel("Taxa de acertos primarios")
	plt.xticks(nBeams)

	plt.subplot(3,1,2)
	plt.errorbar(nBeams,mundiMapp, yerr=mundiMappBar, c='green', fmt='o')
	plt.plot(nBeams, mundiMapp, c='green', label='mundiMapp')

	plt.errorbar(nBeams, goMundi, yerr=goMundiBar, c='black', fmt='o')
	plt.plot(nBeams, goMundi, c='black', label='goMundi')
	plt.xticks(nBeams)
	plt.ylabel("Tempo ($\mu$S)")
	plt.legend(loc=0)

	plt.subplot(3,1,3)
	plt.errorbar(nBeams,mundiMapp, yerr=mundiMappBar, c='green', fmt='o')
	plt.plot(nBeams, mundiMapp, c='green', label='mundiMapp')

	plt.errorbar(nBeams, goMundi, yerr=goMundiBar, c='black', fmt='o')
	plt.plot(nBeams, goMundi, c='black', label='goMundi')
	
	plt.errorbar(nBeams,mdnd, yerr=mdndBar, c='red', fmt='o')
	plt.plot(nBeams, mdnd, c='red', label='MDND')
	plt.ylabel("Temp (S)")
	plt.xlabel("Numero de Nos")
	plt.xticks(nBeams)

	plt.legend(loc=0)
	plt.show()
