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
	dir1 = '/home/dbrilhante/results/sched-norelief-10-43-04-17-08-17'#sys.argv[1]
	dir2 = '/home/dbrilhante/results/sched-relief-17-04-37-17-08-17'#sys.argv[2]
	nNodes = sys.argv[1]
	runs = 30
	nBeams = [4, 8, 16, 32]
	#dev = [0.05, 0.06, 0.07, 0.08, 0.09]
	sep = '-'

	plot = []
	bar = []

	fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

	plot = []
	bar = []		
	for erro in [0,4]:
		for i in nBeams:
			#for h in dev:	
			temp = []
			for j in range(1,runs):
				supra = 1
				filename = dir1+"/"+str(nNodes)+sep+str(i)+sep+str(0)+sep+str(erro)+sep+str(j)
				f = open(filename)
				line = []
				while supra <= 4:
					line += [float(f.readline())]
					#print line
					supra += 1
				#print line
				if sys.argv[2]=="a":
					temp.append(line[1])
				elif sys.argv[2]=="r":
					temp.append(line[3]/line[2])
				elif sys.argv[2]=="t":
					temp.append(line[3])
					
			#print temp
			plot.append(avgCalc(temp))
			bar.append(intervalCalc(temp, 95))
		#print plot, bar

		if erro == 0:
			plt.errorbar(nBeams,plot, yerr=bar, c='red', fmt='o')
			ax.plot(nBeams,plot, 'red', ls='--')
		else:
			plt.errorbar(nBeams,plot[4:], yerr=bar[4:], c='blue', fmt='o')
			ax.plot(nBeams,plot[4:], 'blue', ls='--')

	plot = []
	bar = []		
	for erro in [0,4]:
		for i in nBeams:
			#for h in dev:	
			temp = []
			for j in range(1,runs):
				supra = 1
				filename = dir2+"/"+str(nNodes)+sep+str(i)+sep+str(0)+sep+str(erro)+sep+str(j)
				f = open(filename)
				line = []
				while supra <= 4:
					line += [float(f.readline())]
					#print line
					supra += 1
				#print line
				if sys.argv[2]=="a":
					temp.append(line[1])
				elif sys.argv[2]=="r":
					temp.append(line[3]/line[2])
				elif sys.argv[2]=="t":
					temp.append(line[3])
					
			#print temp
			plot.append(avgCalc(temp))
			bar.append(intervalCalc(temp, 95))
		#print plot, bar
		if erro == 0:
			plt.errorbar(nBeams,plot, yerr=bar, c='red', fmt='o')
			ax.plot(nBeams,plot, 'red')
		else:
			plt.errorbar(nBeams,plot[4:], yerr=bar[4:], c='blue', fmt='o')
			ax.plot(nBeams,plot[4:], 'blue')

	if sys.argv[2]=="a":
		plt.ylabel("Media de tentativas por par")
	elif sys.argv[2]=="r":
		plt.ylabel("Media do Tempo medio de transmissao")
	elif sys.argv[2]=="t":		
		plt.ylabel("Tempo total medio")
	#plt.ylim(0,1)
	plt.xlabel("N BEAMS")
	plt.xticks(nBeams)
	plt.title("Rede com "+str(nNodes)+" nos")
	#plt.xlim(10,50)

	handles, labels = ax.get_legend_handles_labels()
        display = (0,1,2, 3, 4, 5, 6, 7)
        leg1 = plt.Line2D((0,1),(0,0), color='red', linestyle='--')
        leg2 = plt.Line2D((0,1),(0,0), color='red')
        leg3 = plt.Line2D((0,1),(0,0), color='blue', linestyle='--')
        leg4 = plt.Line2D((0,1),(0,0), color='blue')
	list1 = ['Sem folga e sem erros', 'Com folga e sem erros', 'Sem folga e $\sigma$ = 20', 'Com folga e $\sigma$ = 20']
        ax.legend([leg1, leg2, leg3, leg4]+[handle for i,handle in enumerate(handles) if i in display],
         list1+[label for i,label in enumerate(labels) if i in display], loc=0, ncol=1)
        plt.show()
