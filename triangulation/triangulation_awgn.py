#! /usr/bin/python

#import matplotlib.pyplot as plt
import random
import math
import subprocess
import sys

pi = math.pi


class Node:
        def __init__(self,latitude,longitude,sense):
                self.x=latitude
                self.y=longitude
                self.sensibility=sense #node sensibility in dbm
                #The parameter below is like a DIRECTIONAL NETWORK ALLOCATION VECTOR
                self.angleList = [] #list of angles to nodes, index i angle to node i
                self.isLeader = False
                self.north = 0 #if the nodes does not follow the same north as leader
                self.Id = None #the node identification (number, mac, whatever)
                self.angleToLeader = None
                self.adj = []
		self.wifiGain = 5
		self.wifiTxPower = 20

        def setPower (self, power):
                #set node's transmission power
                self.txPower=power
        def setAdj(self,nNodes):
                for i in range(nNodes):
                        self.adj.append(random.gauss(0.5,float(sys.argv[6])))

        def setBeams (self, nBeams):
                #set node's number o beams/sectors
                self.nBeams = nBeams
                #set node's beamwidth
                self.beamwidth = 2*pi/self.nBeams

        def setAntennaGain(self, gain_omni, model):
                if (model=='plain'):
                        self.mainLobeGain = (2*pi/self.nBeams)*gain_omni
                        self.sideLobeGain = 0

                if (model=='log'):
                        self.mainLobeGain = math.log10(2*pi/self.nBeams)*gain_omni
                        self.sideLobeGain = math.log10((2*pi - self.nBeams)/self.nBeams)*gain_omni

def beamforming(nodes, i, j):
        dist = round(math.hypot(nodes[i].x-nodes[j].x,nodes[i].y-nodes[j].y),2)
        angle = math.atan2(nodes[i].y-nodes[j].y, nodes[i].x-nodes[j].x) + pi
        if angle == 2*pi: angle = 0
	beam = int(round(angle/nodes[i].beamwidth,1))
	if i == j: return [0,0,0]
        return [beam,dist,round(angle,2)]


def beamformingReal(nodes, i, j, varD, varA, meand, devd, meana, deva):
	'''The normal function cover 0.9901 percent of the cases for 2.33
	The error is a normal random variable with mean 0.8 and standard deviation
	equal to 0.8/2.33
	Then the resulting error associated with the beamforming measured distance
	is more or less these random variable we just defined'''

	if i == j: return [0,0,0]

	#==== DISTANCE ERROR CALC ====#
	if (meand <> -1) and (devd <> -1):
		if varD == 'normal': erro = random.gauss(meand,devd)#*random.choice([-1,1])
		elif varD == 'log':
			new_meand = math.exp(meand+devd/2)
			new_devd = math.exp(2*meand+devd)*(math.exp(devd)-1)
			erro = random.lognormvariate(new_meand,new_devd)#*random.choice([-1,1])
		else: print 'ERROR! Random Variable not available'
	else: erro = 0
	dist = round(math.hypot(nodes[i].x-nodes[j].x,nodes[i].y-nodes[j].y),2)+erro

	#==== ANGLE ERROR CALC ====#
	if meana <> -1 and deva<>-1:
		if varA == 'normal': erro = random.gauss(meana,deva)#*random.choice([-1,1])
		elif varA == 'log':
			new_meana = math.exp(meana+deva/2)
			new_deva = math.exp(2*meana+deva)*(math.exp(deva)-1)
			erro = random.lognormvariate(new_meana,new_deva)#*random.choice([-1,1])
		else:print 'ERROR! Random Variable not available'
	else: erro = 0
        angle = math.atan2(nodes[i].y-nodes[j].y, nodes[i].x-nodes[j].x) + pi + math.radians(erro)

        if angle == 2*pi: angle = 0
        beam = int(round(angle/nodes[i].beamwidth,1))
        #return [beam,dist,round(angle,5)]
	return [beam,dist,angle]


def estimating(nodes, i, j, leader, maptable):
	if i == j: return [0,0,0]
	angleDiff = abs(maptable[i][0] - maptable[j][0])*nodes[leader].beamwidth
	signal = math.copysign(1, maptable[i][0]-maptable[j][0])

	estimative = math.atan2(maptable[j][1]*math.sin(angleDiff), maptable[i][1] - (maptable[j][1]*math.cos(angleDiff)))


	if(maptable[i][0] > nodes[i].beamwidth/2): nodes[i].angleToLeader = maptable[i][0] - nodes[i].nBeams/2
	else: nodes[i].angleToLeader = maptable[i][0] + nodes[i].nBeams/2

	if nodes[i].angleToLeader < 0: nodes[i].angleToLeader = nodes[i].nBeams + nodes[i].angleToLeader
	#if round(nodes[i].angleToLeader,6) == round(2*pi,6): return [0, round(maptable[i][1],2), 'l']
	if nodes[j].isLeader == True:
		#if round(nodes[i].angleToLeader,2) == round(2*pi,2):
		#	return [0, round(maptable[i][1],2), 'l']
		#else:
		return [nodes[i].angleToLeader, round(maptable[i][1],2), round(nodes[i].angleToLeader,6), 'l' ]

	dist = round(math.sqrt(maptable[i][1]**2+maptable[j][1]**2+2*maptable[i][1]*maptable[j][1]*math.cos(angleDiff)),2)

	if angleDiff==0:
		if maptable[i][1] > maptable[j][1]: return[nodes[i].angleToLeader, dist, round(nodes[i].angleToLeader*nodes[i].beamwidth,2)]
		elif maptable[i][1] < maptable[j][1]:
			if nodes[i].angleToLeader > (nodes[i].nBeams/2 -1):
				return[nodes[i].angleToLeader - nodes[i].nBeams/2, dist, round((nodes[i].angleToLeader- nodes[i].nBeams/2)*nodes[i].beamwidth,2)]
			elif nodes[i].angleToLeader < (nodes[i].nBeams/2 -1):
				return[nodes[i].angleToLeader + nodes[i].nBeams/2, dist, round((nodes[i].angleToLeader+ nodes[i].nBeams/2)*nodes[i].beamwidth,2)]

	if (signal>0):
		a = round(nodes[i].angleToLeader*nodes[i].beamwidth+estimative,1)
		a2 = nodes[i].angleToLeader*nodes[i].beamwidth+estimative
		beam = int(round(((nodes[i].angleToLeader+0.5)*nodes[i].beamwidth + estimative)/nodes[i].beamwidth,1))#,dist,1]
		beam =  int(round(((nodes[i].angleToLeader+nodes[i].adj[j])*nodes[i].beamwidth + estimative)/nodes[i].beamwidth,1))
		#beam = int(a/nodes[i].beamwidth)
	else:
		a = round(nodes[i].angleToLeader*nodes[i].beamwidth-estimative,1)#, dist,2]
		a2 = nodes[i].angleToLeader*nodes[i].beamwidth-estimative
		beam =  int(round(((nodes[i].angleToLeader+0.5)*nodes[i].beamwidth - estimative)/nodes[i].beamwidth,1))
        	#print i, j
		beam =  int(round(((nodes[i].angleToLeader+nodes[i].adj[j])*nodes[i].beamwidth - estimative)/nodes[i].beamwidth,1))
		#beam = int(a/nodes[i].beamwidth)

	if (a < 0):
		beam = int(round((2*pi + a2)/nodes[i].beamwidth,1))
		#a = round(2*pi + (nodes[i].angleToLeader - estimative),2)
		a = round(2*pi + a2, 2)

	#elif (a > round(2*pi, 2)): beam = int(round((a2 - 2*pi)/nodes[i].beamwidth,1))

	if (beam >= nodes[i].nBeams):
		a = round(a2 - 2*pi, 2)
		beam = beam - nodes[i].nBeams

	if a == round(2*pi,2): beam = 0
	return [beam, dist, a]
	#'''

def txSched(nodes,nNodes):
	total = (nNodes-1)*(nNodes-2)
	ntx = random.randint(total/2,total-1)
	transmissions = []
	for i in range(ntx): transmissions.append([])
	seq = []
	for i in range(nNodes): seq = seq + [i]

	for i in range(ntx):
		x=0
		y=0
		while x == y:
			x = random.choice(seq)
			y = random.choice(seq)

		transmissions[i] = [x,y]

	return transmissions

def txCheck(nodes, proof, tx, rx, tdict):
	time = 0
	check = False
	i = 1
	signal = random.choice([-1,1])
	#attempt = random.choice([-1,1])
	while  check == False:
		#if i <> 1:
		attempt = -1*signal*i
		signal = signal*-1
		#print attempt, i
		#raw_input()
        #the sector obtained from lider is ok!
		if nodes[tx].angleList[rx][0] == proof[tx][rx][0]: 
			time = tdict['txData']
			check =True
        #The sector obtained is not ok, but we will alleviate
		elif int(sys.argv[5])==1 and abs(nodes[tx].angleList[rx][0] - proof[tx][rx][0]) <= 1:
			time = tdict['txData']
			check =True
        #The sector is not ok and we will guess another adjacent sector
		else:
			nodes[tx].angleList[rx][0] += attempt
			if nodes[tx].angleList[rx][0] < 0: nodes[tx].angleList[rx][0] = nodes[tx].nBeams + nodes[tx].angleList[rx][0]
			elif nodes[tx].angleList[rx][0] > nodes[tx].nBeams -1: 
				nodes[tx].angleList[rx][0] = nodes[tx].angleList[rx][0] - nodes[tx].nBeams
			time += tdict['txData']+tdict['waitAck']	
			i += 1
	time += tdict['txAck']
	return [i, time]


'''
def drawNetwork(nodes):
	plt.ylim(-6,6)
	plt.xlim(-6,6)
	x = []
	y = []
	for i in nodes:
		x.append(i.x)
		y.append(i.y)
	plt.xticks(x)
	plt.yticks(y)
	plt.plot(x,y, 'ro', ms=20)
	plt.grid(True)
	plt.show()
'''

if __name__ == "__main__":
	nNodes = int(sys.argv[1])
	nBeams = int(sys.argv[2])
        nodes = []
        latitude=10
        longitude = 10
        leader = 0#int(sys.argv[1])
        #chosen = int (sys.argv[2])
        seed = int(sys.argv[7])#5])
	relief = int(sys.argv[5])
        random.seed(seed)

	time_arr = {'txAck':1,
			'bf':1,
		    	'waitAck':1,
			'txData':1,
			'txMap':1,
			'txRts':1, 
			'txCts':1, 
			'txNum':1}
	

	'''-------- PREPARING ERROR ---------'''
	indexd = int(sys.argv[3])
	indexa = int(sys.argv[4])

	#==== DEFINING ARRAYS ====#
	#meand = []
	#devd = [-1, 0.781, 0.869, 0.961, 1.075, 1.190]
	meand = [-1, 0.1,0.2,0.3,0.4,0.5,0.6]
	devd = [-1, 1.0,1.2,1.4,1.6,1.8,2.0]
	#meana = []
	deva = [-1, 5, 10, 15, 20]

	#==== GETTING VALUES ====#
	#mu_d = 0 #meand[indexd]
	mu_d = meand[indexd]
	sigma_d = devd[indexd]
	mu_a = 0 #meana[indexa]
	sigma_a = deva[indexa]

	'''-------- END OF ERROR ------------'''

	lista = []
	nodes.append(Node(0,0,20))
	nodes[leader].Id = 0
	nodes[leader].setBeams(nBeams)
	lista.append([nodes[leader].x, nodes[leader].y])
        for i in range(1,nNodes):
                nodes.append(Node(random.randint(-(latitude/2),latitude/2),random.randint(-(longitude/2),longitude/2),20))
                nodes[i].Id = i
                nodes[i].setAdj(nNodes)
		nodes[i].setBeams(nBeams)
                while (lista.count([nodes[i].x, nodes[i].y])<>0):
                        nodes[i].x = random.randint(-(latitude/2),latitude/2)
                        nodes[i].y = random.randint(-(longitude/2),longitude/2)
                lista.append([nodes[i].x, nodes[i].y])
		#print i, nodes[i].x, nodes[i].y
	nodes[leader].isLeader = True
	nodes[leader].setAdj(nNodes)
	num = 0
	den = 0

	#drawNetwork(nodes)

	#proof = [] #list to save the correct beamforming and compare with proposed algorithm
	for i in range(nNodes):
		nodes[leader].angleList.append(beamformingReal(nodes,leader,i,'normal','normal', mu_d, sigma_d, mu_a, sigma_a))
	#print nodes[leader].angleList


	proof=[]
	fair=[]
	ang_err = 0
	b=0
	count=0
	for j in range(nNodes):
		a = 0
		temp = []
		chosen = j
		for i in range(nNodes):
			nodes[chosen].angleList.append(estimating(nodes,chosen, i, leader, nodes[leader].angleList))
			temp.append(beamforming(nodes,chosen,i))
			#print proof[i], nodes[chosen].angleList[i]
		proof.append(temp)

		template = "{0:15}"
		for i in range(nNodes):
			den = den + 1
			#print template.format(proof[i]),
			#print template.format(nodes[chosen].angleList[i]),
			if relief == 0:
				if temp[i][0] <> nodes[chosen].angleList[i][0]:
					#===== uncomment below for log =====
					#print chosen, i, "--->",
					#print template.format(temp[i]),
                                	#print template.format(nodes[chosen].angleList[i])
					ang_err = ang_err + abs(temp[i][2] - nodes[chosen].angleList[i][2])
					num = num + 1
					a += 1
				else:#count the average error when some node is rigth
					b += abs(temp[i][2] - nodes[chosen].angleList[i][2])
					count+=1
			else:
				if abs(temp[i][0] - nodes[chosen].angleList[i][0])>1:
					if not ((temp[i][0]==0 and nodes[chosen].angleList[i][0]==nodes[chosen].nBeams-1)
					or (temp[i][0]==nodes[chosen].nBeams-1 and nodes[chosen].angleList[i][0]==0)):
						#===== uncomment below for log =====
						#print chosen, i, "--->",
						#print template.format(temp[i]),
						#print template.format(nodes[chosen].angleList[i])
						ang_err = ang_err + abs(temp[i][2] - nodes[chosen].angleList[i][2])
						num = num + 1
						a +=1
					else:
						b += abs(temp[i][2] - nodes[chosen].angleList[i][2])
						count+=1

				else:
					b += abs(temp[i][2] - nodes[chosen].angleList[i][2])
					count+=1
		fair.append(a)

	part = 0
	#for i in fair: part += i**2
	#fairness = 1.0*sum(fair)**2/(nNodes*part)
				#print template.format(proof[i]),
				#print template.format(nodes[chosen].angleList[i]),
				#print "-----> ERROR sectorized2.py", leader, chosen, seed
			#else: print "\n",'''

	print round(1.0*num/den,6)#number of errors
	#UNCOMMENT THIS LATER!!!
	#if num <> 0: print round(1.0*ang_err/num, 6)#average erro in radians
	#else: print 0.0
	#print round(1.0*b/count,6)

	#print round(fairness,6)
	#fair = range(nNodes)
	for i in fair: fair[i]=0
	num = 0
	den = 0
	overhead = (time_arr['bf']*nNodes*nBeams**2)+time_arr['txNum']+time_arr['txMap']
	schedule = txSched(nodes,nNodes)
	#print schedule
	for i in schedule:
		overhead += time_arr['txRts']+time_arr['txCts']
		#print i[0], nodes[i[0]].x, nodes[i[0]].y, '|', i[1], nodes[i[1]].x,nodes[i[1]].y, nodes[i[0]].angleList[i[1]][0]
		den += 1
		a, time = txCheck(nodes,proof,i[0],i[1], time_arr)
		overhead += time
		#fair[i[0]]+=a
		num += a

	print round(1.0*num/den,6)
	print overhead
	part = 0
	for i in fair: part += i**2
	fairness = 1.0*sum(fair)**2/(nNodes*part)
