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

abftSlots = int(sys.argv[3])
nNodes = int(sys.argv[4])
#cWindow = int(sys.argv[5])
prob = []
time = []

beaconInterval = 200
beaconDur = 0.1
abftDur = 0.1
slotDur = 1

for i in covered:
	soma = 0
	p = (1.0/sta.quasiomni)*(1.0*i/ap.nbeams)
	bernoulli1 = 1.0 - (1.0 - p)**i
	bernoulli2 = nNodes*(1.0/abftSlots)*(1.0 - 1.0/abftSlots)**(nNodes-1) 
	prob.append(bernoulli1*bernoulli2)

	comp1 = (1 - bernoulli1)*beaconInterval
	comp2 = bernoulli1*beaconDur
	comp3 = bernoulli2*abftDur
	comp4 = (1-bernoulli2)*(beaconInterval - abftDur)

	time.append(comp1+comp2+comp3+comp4)

print prob
print time
