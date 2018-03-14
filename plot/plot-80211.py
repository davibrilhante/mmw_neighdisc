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
	dir1 = '/home/davi/validation' #/mmw/Julho/18-1/sector-norelief-01-22-07-17-07-17 #sys.argv[1]
	dir2 = '/home/dbrilhante/Documents/Codes/mmw/Julho/awgn-norelief-01-36-33-20-07-17'#sys.argv[2]
	#nBeams = sys.argv[1]
	runs = 40
	nNodes = [5, 10, 15, 20, 25, 50, 100] #[10, 20, 30, 40]
	std = [7]#, 29] #[0.05, 0.06, 0.07, 0.08, 0.09]
	sep = '-'
	SLRC = [4, 8, 16, 32]

	tx_rate = 6#e6
	slot = 9
	delta_tx = 60*8.0/tx_rate
	delta_sifs = 10
	delta_difs = 28
	delta_ack = 32.0*8.0/tx_rate
	delta_timeout = 100

	plot = []
	bar = []

	fig = plt.figure()
        ax = fig.add_subplot(1,1,1)

	'''for s in std:
		plot = []
		bar = []		
		for n in nNodes:	
			temp = []
			counter=0
			#for j in range(1,runs):
			j=1
			while counter <> 29:
				filename = dir1+"/"+str(n)+sep+str(s)+sep+str(j)
				f = open(filename)
				check = f.readline()	
				check = float(check)
				j+=1
				print counter, j
				if ((n==30 and check<4) or (n==40 and check<=11) or (n==10 and check==0) or (n==20 and check==0)):
					#print "entra"	
					time = f.readline()
					#print time
					temp.append(float(time))
					counter+=1
				else:
					pass
				if float(time) < 0.0:
					print "entrou"
					temp.pop()
					counter -=1
					pass
				#if counter==30:
				#	break
			print temp,"\n"
			plot.append(avgCalc(temp))
			bar.append(intervalCalc(temp, 95))
		if std == 7:
			plt.errorbar(nNodes,plot, yerr=bar, c='red', fmt='o')
			ax.plot(nNodes,plot, 'red', ls='--')
		else:
			plt.errorbar(nNodes,plot, yerr=bar, c='blue', fmt='o')
			ax.plot(nNodes,plot, 'blue', ls='--', label='Simulated')'''

	plt.ylabel("TAXA MEDIA DE ACERTOS PRIMARIOS")
	#plt.ylim(0,1)
	plt.xlabel("N NOS")
	#plt.xlim(10,50)
	for slrc in SLRC: 
		w=16
		#slrc=6
		tx_time=[]
		plotter = []
		for n in nNodes:
			cumul = 0
			for s in range(1,slrc):
				prod = 1
				for k in range(1,s):
					#if ((2**k)*w) <= 1024:
					tau_k = 2.0/((2**k)*w+1.0)

					pt = 1.0 - (1.0 - tau_k)**n
					ps = tau_k*(1.0 - tau_k)**(n-1)/pt

					expected_col = (1.0 - n*ps)
					prod = prod*expected_col

				tau_s = 2.0/((2**s)*w+1.0)
				pt = 1.0 - (1.0 - tau_s)**n
				ps = tau_s*(1.0 - tau_s)**(n-1)/pt
				expected_tx = (n*ps)#(delta_tx+delta_difs+delta_ack+delta_sifs)*k

				cumul += prod*expected_tx*s

			plotter.append(cumul)#expected_bo+expected_tx+expected_col)
			backoff = 0
			for a in range(int(cumul)):
				backoff += (((2**a)*w)-1.0)*slot/2

			time = delta_difs + backoff + (math.ceil(cumul)+1)*(delta_sifs+delta_ack+delta_tx)
			time = time*(n-2)*(n-1)
			#tx_time.append(time/1e6)

			for a in range(1,n):
				cumul = 0
				for s in range(1,8):
					prod = 1
					for k in range(1,s):
						if ((2**k)*w) <= 1024:
							tau_k = 2.0/((2**k)*w+1.0)

						pt = 1.0 - (1.0 - tau_k)**a
						ps = tau_k*(1.0 - tau_k)**(a-1)/pt

						expected_col = (1.0 - a*ps)
						prod = prod*expected_col

					tau_s = 2.0/((2**s)*w+1.0)
					pt = 1.0 - (1.0 - tau_s)**a
					ps = tau_s*(1.0 - tau_s)**(a-1)/pt
					expected_tx = (a*ps)

					cumul += prod*expected_tx*s

				backoff = 0
				for a in range(int(cumul)):
					backoff += (((2**a)*w)-1.0)*slot/2

				time += delta_difs + backoff + (math.ceil(cumul)+1)*(delta_sifs+delta_ack+delta_tx)
			tx_time.append(time/1e6)

		plt.plot(nNodes,tx_time, 'r', label='Analytical')
		'''
		handles, labels = ax.get_legend_handles_labels()
		display = (0,1,2, 3, 4, 5, 6, 7)
		leg1 = plt.Line2D((0,1),(0,0), color='red', linestyle='--')
		leg2 = plt.Line2D((0,1),(0,0), color='red')
		leg3 = plt.Line2D((0,1),(0,0), color='blue', linestyle='--')
		leg4 = plt.Line2D((0,1),(0,0), color='blue')
		list1 = ['Sem folga e sem erros', 'Com folga e $\sigma$=20', 'Sem folga e sem erros', 'Sem folga e $\sigma$ = 20']
		ax.legend([leg2, leg4, leg1, leg3]+[handle for i,handle in enumerate(handles) if i in display],
		 list1+[label for i,label in enumerate(labels) if i in display], loc=0, ncol=2)
		'''
		plotter = []
		time = 0
		tau=2.0/(w+1)
		for n in nNodes:
			pt = 1.0 - (1.0 - tau)**n
			ps = n*tau*((1-tau)**(n-1))/pt

			expected_bo = (1-pt)*slot

			expected_tx = (ps*pt)*(delta_tx+delta_difs+delta_ack+delta_sifs)
			expected_col = (1.0 - ps)*pt*(delta_tx+delta_difs+delta_timeout)

			#plotter.append(5*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6))
			time = (n*(n-2))*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6)
			for k in range(1,n):
				pt = 1.0 - (1.0 - tau)**k
				ps = k*tau*((1-tau)**(k-1))/pt

				expected_bo = (1-pt)*slot

				expected_tx = (ps*pt)*(delta_tx+delta_difs+delta_ack+delta_sifs)
				expected_col = (1.0 - ps)*pt*(delta_tx+delta_difs+delta_timeout)

				time += (expected_bo+expected_tx+expected_col)/(ps*pt*1e6)
				#plotter.append(5*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6))
			plotter.append(time)
	#plt.plot(nNodes,plotter,'g',label="mdnd")
	#plt.ylabel("Expected transmissions $(s)$")

	plt.legend(loc=0)
	plt.show()
