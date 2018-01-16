import matplotlib.pyplot as plt
import math
import random
import sys

class Node:
	def __init__(self, nBeams, quasiOmni):
		self.nbeams = nBeams
		self.quasiomni = quasiOmni

ap = Node(int(sys.argv[1]), int(sys.argv[2]))
sta = Node(int(sys.argv[1]), int(sys.argv[2]))

covered = range(1,ap.nbeams/2+1)

abftSlots = [8, 12, 16, 20, 24] #int(sys.argv[3])
nNodes = int(sys.argv[3])
cWindow = int(sys.argv[4])
prob = []
time = []

beaconInterval = 200
beaconDur = 0.1
abftDur = 0.1
slotDur = 1
for j in abftSlots:
	temp1 = []
	temp2 = []
	for i in covered:
		soma = 0
		p = (1.0/sta.quasiomni)*(1.0*i/ap.nbeams)
		bernoulli1 = 1.0 - (1.0 - p)**i
		bernoulli2 = math.exp(-1.0/j)#nNodes*(1.0/j)*(1.0 - 1.0/j)**(nNodes-1)
		#for m in range(2,nNodes+1): bernoulli2 = bernoulli2 + (1/(j**m))
		#temp.append(bernoulli2)
		feedback = (2.0*nNodes/(1.0*cWindow+1))*((1.0*cWindow -1)/(1.0*cWindow+1))**nNodes/(1 -((1.0*cWindow -1)/(1.0*cWindow+1))**nNodes)
		temp1.append(bernoulli1*bernoulli2)#*feedback)

		comp1 = (1 - bernoulli1)*beaconInterval
		comp2 = bernoulli1*beaconDur
		comp3 = bernoulli2*abftDur
		comp4 = (1-bernoulli2)*(beaconInterval - abftDur)

		temp2.append(comp1+comp2+comp3+comp4)
	prob.append(temp1)
	time.append(temp2)
	plt.plot(covered, temp1,label=str(j)+" slots")
	plt.plot(covered, temp2)

#print prob
#print time
plt.ylim(0,1)
plt.legend(loc=0)
plt.show()
