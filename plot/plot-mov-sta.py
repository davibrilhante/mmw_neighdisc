import matplotlib.pyplot as plt
import math
import sys

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
        dir1 = "/home/davi/outputs/12-25-39-08-03-18/"#10-31-16-22-02-18/"#09-08-01-22-02-18/"
        dir2 = "/home/davi/outputs/09-24-31-22-02-18/"

        nNodes = [5, 10, 15, 20, 25]
        nBeams = [8, 16, 32]
        meand = "2"
        meana = "2"
        relief = ["0","1"]
        runs = 30
	sep = "-"
	discarded = []
	discardedError = []
	timeMov = []
	timeMovError = []
	timeSta = []
	timeStaError = []

	container = [[],[],[],[],[],[]]

	font = {'family' : 'normal',
        'size'   : 18}

        plt.rc('font', **font)


	for n in nNodes:
                plot = []
                errorBars = []
                for r in range(1,runs):
                        lineCounter=0
                        filename = dir1+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+str(r)
                        f = open(filename)
                        while lineCounter < 6:
                                if lineCounter == 0 or lineCounter == 3:
                                        container[lineCounter].append(float(f.readline()))
                                else:
                                        container[lineCounter].append(float(f.readline()))

                                lineCounter += 1
                        f.close()

		timeMov.append(avgCalc(container[3]))
		discarded.append(avgCalc(container[5]))
		
		timeMovError.append(intervalCalc(container[3],95))
		discardedError.append(intervalCalc(container[5],95))

	container = [[],[],[],[]]
	for n in nNodes:
                plot = []
                errorBars = []
                for r in range(1,runs):
                        lineCounter=0
                        filename = dir2+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+str(r)
                        f = open(filename)
                        while lineCounter < 4:
                                if lineCounter == 0 or lineCounter == 3:
                                        container[lineCounter].append(float(f.readline()))
                                else:
                                        container[lineCounter].append(float(f.readline()))

                                lineCounter += 1
                        f.close()

		timeSta.append(avgCalc(container[3]))
		timeStaError.append(intervalCalc(container[3],95))
	if sys.argv[1]=="1":	
		plt.errorbar(nNodes,timeSta,yerr=timeStaError,c="red")
		plt.plot(nNodes,timeSta,c="red", label="No Movement")
		plt.errorbar(nNodes,timeMov,yerr=timeMovError,c="blue")
		plt.plot(nNodes,timeMov,c="blue", label="Movement")
		plt.xlabel("Number of Nodes")
		plt.ylabel("Total Time [s]")
	if sys.argv[1]=="2":
		plt.errorbar(nNodes,discarded, yerr=discardedError, c="blue")
		plt.plot(nNodes,discarded,label="Delivery Rate", c="blue")
		plt.xlabel("Number of Nodes")
		plt.ylabel("Delivery Rate %")
	plt.legend(loc=0,fontsize=16)
	plt.show()
