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
        dir1 = "/home/davi/outputs/11-24-41-14-03-18/"#13-07-57-14-03-18/"#10-31-16-22-02-18/"#09-08-01-22-02-18/"
        dir2 = "/home/davi/outputs/11-40-42-14-03-18/"#12-59-21-14-03-18/"#11-40-42-14-03-18/"#09-24-31-22-02-18/"

        nNodes = [5, 10, 15, 20, 25]
	nPeople = [5,6,7,8,9,10]
        nBeams = [8, 16, 32]
        meand = "4"
        meana = "3"
        relief = ["0","1"]
        runs = 30
	sep = "-"
	discarded = []
	discardedError = []
	timeMov = []
	timeMovError = []
	timeRelay = []
	timeRelayError = []
	discardedRelay = []
	discardedRelayError = []

	container = [[],[],[],[],[],[], [], [], []]

	font = {'family' : 'normal',
        'size'   : 18}

        plt.rc('font', **font)


	for n in nNodes:
                plot = []
                errorBars = []
                for r in range(1,runs):
                        lineCounter=0
                        filename = dir1+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+str(nPeople[5])+sep+str(r)
                        f = open(filename)
                        while lineCounter < 9:
                                if lineCounter == 0 or lineCounter == 3:
                                        container[lineCounter].append(float(f.readline()))
                                else:
                                        container[lineCounter].append(float(f.readline()))

                                lineCounter += 1
                        f.close()

		timeRelay.append(avgCalc(container[3]))
		discardedRelay.append(avgCalc(container[8]))
		
		timeRelayError.append(intervalCalc(container[3],95))
		discardedRelayError.append(intervalCalc(container[8],95))

	container = [[],[],[],[], [], []]
	for n in nNodes:
                plot = []
                errorBars = []
                for r in range(1,runs):
                        lineCounter=0
                        filename = dir2+str(n)+sep+str(nBeams[1])+sep+meand+sep+meana+sep+str(nPeople[5])+sep+str(r)
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

	if sys.argv[1]=="1":	
		plt.errorbar(nNodes,timeRelay,yerr=timeRelayError,c="red")
		plt.plot(nNodes,timeRelay,c="red", label="Relay")
		plt.errorbar(nNodes,timeMov,yerr=timeMovError,c="blue")
		plt.plot(nNodes,timeMov,c="blue", label="No Relay")
		plt.xlabel("Number of Nodes")
		plt.ylabel("Total Time [s]")
	if sys.argv[1]=="2":
		plt.errorbar(nNodes,discarded, yerr=discardedError, c="blue")
		plt.plot(nNodes,discarded, c="blue", label="No Relay")
		plt.errorbar(nNodes,discardedRelay, yerr=discardedRelayError, c="red")
		plt.plot(nNodes,discardedRelay, c="red", label="Relay")
		plt.xlabel("Number of Nodes")
		plt.ylabel("Delivery Rate %")
	plt.legend(loc=0,fontsize=16)
	plt.show()
