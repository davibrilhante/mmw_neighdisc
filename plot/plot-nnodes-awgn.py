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
	dir1 = '/home/dbrilhante/Documents/Codes/mmw/Julho/18-1/sector-norelief-01-22-07-17-07-17'#sys.argv[1]
	dir2 = '/home/dbrilhante/Documents/Codes/mmw/Julho/awgn-norelief-01-36-33-20-07-17'#sys.argv[2]
	nBeams = sys.argv[1]
	runs = 20
	nNodes = [10, 30, 50]
	dev = [0.05, 0.07, 0.09]
	sep = '-'

	plot = []
	bar = []

	fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

	for erro in [0,4]:
		plot = []
		bar = []
		for i in nNodes:		
			temp = []
			for j in range(1,runs):
				filename = dir1+"/"+str(i)+sep+str(nBeams)+sep+str(0)+sep+str(erro)+sep+str(j)
				f = open(filename)
				line = f.readline()			
				temp.append(1 - float(line))

			plot.append(avgCalc(temp))
			bar.append(intervalCalc(temp, 95))
		if erro == 0:		
			plt.errorbar(nNodes,plot, yerr=bar, c='red', fmt='o')
			ax.plot(nNodes,plot, 'red')
		else:
			plt.errorbar(nNodes,plot, yerr=bar, c='blue', fmt='o')
			ax.plot(nNodes,plot, 'blue')
			

		for h in dev:	
			plot = []
			bar = []		
			for i in nNodes:
				temp = []
				for j in range(1,runs):
					filename = dir2+"/"+str(i)+sep+str(nBeams)+sep+str(0)+sep+str(erro)+sep+str(h)+sep+str(j)
					f = open(filename)
					line = f.readline()
					temp.append(1 - float(line))

				plot.append(avgCalc(temp))
				bar.append(intervalCalc(temp, 95))
			if erro == 0:
				if h == 0.05:
					plt.errorbar(nNodes,plot, yerr=bar, c='red', fmt='o')
					ax.plot(nNodes,plot, 'red', ls='--')
				elif h == 0.07:
					plt.errorbar(nNodes,plot, yerr=bar, c='red', fmt='^')
					ax.plot(nNodes,plot, 'red', ls='--')
				elif h == 0.09:
					plt.errorbar(nNodes,plot, yerr=bar, c='red', fmt='s')
					ax.plot(nNodes,plot, 'red', ls='--')
			else:
				if h == 0.05:
					plt.errorbar(nNodes,plot, yerr=bar, c='blue', fmt='o')
					ax.plot(nNodes,plot, 'blue', ls='--')
				elif h == 0.07:
					plt.errorbar(nNodes,plot, yerr=bar, c='blue', fmt='^')
					ax.plot(nNodes,plot, 'blue', ls='--')
				elif h == 0.09:
					plt.errorbar(nNodes,plot, yerr=bar, c='blue', fmt='s')
					ax.plot(nNodes,plot, 'blue', ls='--')

	plt.ylabel("TAXA MEDIA DE ACERTOS PRIMARIOS")
	plt.ylim(0,1)
	plt.xlabel("N NOS")
	plt.xlim(10,50)

	handles, labels = ax.get_legend_handles_labels()
        display = (0,1,2, 3, 4, 5, 6, 7)
        leg1 = plt.Line2D((0,1),(0,0), color='red', linestyle='--')
        leg2 = plt.Line2D((0,1),(0,0), color='red')
        leg3 = plt.Line2D((0,1),(0,0), color='blue', linestyle='--')
        leg4 = plt.Line2D((0,1),(0,0), color='blue')
	list1 = ['Sem folga e sem erros', 'Com folga e $\sigma$=20', 'Sem folga e sem erros', 'Sem folga e $\sigma$ = 20']
        ax.legend([leg2, leg4, leg1, leg3]+[handle for i,handle in enumerate(handles) if i in display],
         list1+[label for i,label in enumerate(labels) if i in display], loc=0, ncol=2)
        plt.show()
