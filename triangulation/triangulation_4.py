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
		self.omniWidth = 3

        def setPower (self, power):
                #set node's transmission power
                self.txPower=power
        def setAdj(self,nNodes):
                for i in range(nNodes):
                        self.adj.append(random.gauss(0.5,0.05))

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
	#ntx = random.randint(total/2,total-1)
	transmissions = []
	#for i in range(total): transmissions.append([])
	seq = []
	for i in range(1,nNodes): seq.append(i)

	for x in seq:
		for j in range(nNodes-2):
			y=random.choice(seq)
			while x == y or  transmissions.count([x,y])!=0:
				#x = random.choice(seq)
				y = random.choice(seq)

			transmissions.append([x,y])

	random.shuffle(transmissions)
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
			time += tdict['txData']+tdict['mmwsifs']
			check =True
        #The sector obtained is not ok, but we will alleviate
		elif int(sys.argv[5])==1 and abs(nodes[tx].angleList[rx][0] - proof[tx][rx][0]) <= 1:
			time += tdict['txData']+tdict['mmwsifs']
			check =True
        #The sector is not ok and we will guess another adjacent sector
		else:
			nodes[tx].angleList[rx][0] += attempt
			if nodes[tx].angleList[rx][0] < 0: nodes[tx].angleList[rx][0] = nodes[tx].nBeams + nodes[tx].angleList[rx][0]
			elif nodes[tx].angleList[rx][0] > nodes[tx].nBeams -1: 
				nodes[tx].angleList[rx][0] = nodes[tx].angleList[rx][0] - nodes[tx].nBeams
			time += tdict['txData']+tdict['acktimeout']	
			i += 1
	time += tdict['ack']
	# Returns the time spent to transmit the information, 
	# taking in count the possible retransmissions and the 
	# time to find the right beam to neighbor
	return [i, time]


def projections(r,node, adj):
        precision = 3
        Projection = []
        alpha = 2*pi/node.nBeams
        for n in range(node.nBeams):
                if (n*alpha < pi) and (n*alpha< adj) and ((n+1)*alpha-adj > adj):
                        x1 = node.x
                        x2 = node.x + r
                elif (n*alpha < pi) and (n*alpha< pi+adj) and ((n+1)*alpha > pi+adj):
                        x1 = node.x
                        x2 = node.x - r
                else:
                        x1 = node.x + r*math.cos(n*alpha-adj)
                        x2 = node.x + r*math.cos((n+1)*alpha-adj)
                        #x = max(x1,x2) 
                if x1< node.x and x2<node.x:
                        if x1<x2: x2 = node.x
                        else: x1 = node.x
                elif x1> node.x and x2>node.x:
                        if x1<x2: x1 = node.x
                        else: x2 = node.x

                if (n*alpha < pi) and (n*alpha < (pi/2)+adj) and ((n+1)*alpha > (pi/2)+adj):
                        y1 = node.y + r
                        y2 = node.y
                elif (n*alpha > pi) and (n*alpha < (3*pi/2)+adj) and ((n+1)*alpha > (3*pi/2)+adj):
                        y1 = node.y
                        y2 = node.y - r
                else:
                        y1 = node.y + r*math.sin(n*alpha-adj)
                        y2 = node.y + r*math.sin((n+1)*alpha-adj)

                if y1< node.y and y2<node.y:
                        if y1<y2: y2 = node.y
                        else: y1 = node.y
                elif y1> node.y and y2>node.y:
                        if y1<y2: y1 = node.y
                        else: y2 = node.y

                Projection.append([[round(x1,precision),round(x2,precision)],
                                   [round(y1,precision),round(y2,precision)]])
                #print "[",x1,",",x2,"] [",y1,",",y2,"]"
        return Projection

def intersections(i, j, ri, rj):        #(arrayI, arrayJ):
        theta1 = math.atan2(j.y-i.y,j.x-i.x)
        theta2 = math.atan2(i.y-j.y,i.x-j.x)
        if theta1 < 0: theta1 = 2*pi + theta1
        if theta2 < 0: theta2 = 2*pi + theta2

        #print math.degrees(theta1), math.degrees(theta2)
        d = math.hypot(i.x-j.x, i.y-j.y)
        delta = 0.25*(math.sqrt((d+ri+rj)*(d+ri-rj)*(d-ri+rj)*(-d+ri+rj)))
        x1 = ((i.x+j.x)/2) + ((j.x-i.x)*((ri**2)-(rj**2))/(2*d**2)) + (2*(i.y-j.y)*delta/(d**2))
        x2 = ((i.x+j.x)/2) + ((j.x-i.x)*((ri**2)-(rj**2))/(2*d**2)) - (2*(i.y-j.y)*delta/(d**2))
        y1 = ((i.y+j.y)/2) + ((j.y-i.y)*((ri**2)-(rj**2))/(2*d**2)) - (2*(i.x-j.x)*delta/(d**2))
        y2 = ((i.y+j.y)/2) + ((j.y-i.y)*((ri**2)-(rj**2))/(2*d**2)) + (2*(i.x-j.x)*delta/(d**2))

        #print x1,y1,x2,y2
        alpha=[0,0,0,0]
        alpha[0] = math.atan2(y1 - i.y,x1 - i.x)
        alpha[1] = math.atan2(- i.y + y2,-i.x + x2)

        alpha[2] = math.atan2(y1 - j.y,x1 - j.x)
        alpha[3] = math.atan2(y2 - j.y,x2 - j.x)
        widthI = max(alpha[0],alpha[1]) - min(alpha[0],alpha[1])
        widthJ = max(alpha[2],alpha[3]) - min(alpha[2],alpha[3])
        #print math.degrees(alpha[0]), math.degrees(alpha[1]), math.degrees(alpha[2]), math.degrees(alpha[3])
        for m in range(len(alpha)):
                if alpha[m] < 0:
                        alpha[m] = 2*pi + alpha[m]
                #print math.degrees(alpha[m])

        #print math.degrees(widthI), math.degrees(widthJ)

	distI = math.hypot(i.x-x2, i.y-y2)
        distJ = math.hypot(j.x-x2, j.y-y2)

        deltaI = math.atan2(i.y-y2,i.x-x2) - theta1
        deltaJ = math.atan2(j.y-y2,j.x-x2) - theta1
        #print math.degrees(deltaI), math.degrees(deltaJ)

        newI = Node(distI*math.cos(deltaI), distI*math.sin(deltaI), 10)
        newJ = Node(distJ*math.cos(deltaJ), distJ*math.sin(deltaJ), 10)
        newI.setBeams(i.nBeams)
        newJ.setBeams(j.nBeams) #to receiver we will set the quasi omni mode

        #print newI.x, newI.y, newJ.x, newJ.y

        projectionsI = projections(d, newI, theta1)
        projectionsJ = projections(d, newJ, theta1)
        #print projectionsI
        #print projectionsJ
        array = []
        countI=0
        for m in projectionsI:
                countJ=0
                for n in projectionsJ:
                        if  not ((max(n[0][0],n[0][1])<=min(m[0][0],m[0][1])) or (min(n[0][0],n[0][1]) >= max(m[0][1],m[0][0]))):
                                if not((max(n[1][0],n[1][1])<=min(m[1][0],m[1][1])) or (min(n[1][0],n[1][1]) >= max(m[1][1],m[1][0]))):
                                        array.append([countI,countJ])
                        countJ+=1
                countI+=1
        return array


def overhear(i, j):
	original = i.nBeams
	i.setBeams(i.omniWidth)
	r = math.hypot(i.x-j.x, i.y-j.y)
        #Here starts an algorithm to detect an intersection betwen beams
        #The instersection of projections:
        #i is in quasi omni mode

        array = intersections(i,j,r,r)#(projectionsI, projectionsJ)
        p=[]
        for m in range(i.nBeams):
                count = 0
                for n in array:
                        #print n
                        if n[0]==m:
                                count +=1
                #print count
                if count<>0: p.append((1.0*count/j.nBeams)*(1.0/i.nBeams))
                else: p.append(0)

        #print p
	#P=0
	#for m in p:
	#	P += m
        P = p[0]+p[1]+p[2]
        choice = [1]*int(P*100) + [0]*int((1-P)*100)
	#print P, choice
	i.setBeams(original)
        return random.choice(choice)

def wifiModel(cw_min, nNodes,delta_difs, delta_sifs, payload, 
	     delta_ack, delta_timeout, slot, slrc, wifi_rate ):
	delta_tx = (payload*8.0)/wifi_rate #time to transmit the frame im micro seconds
	w = cw_min
	n = nNodes
	time=0
	cumul = 0
	for s in range(1,slrc):
		prod = 1
		for k in range(1,s):
			if ((2**k)*w) <= 1024:
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

	#plotter.append(cumul)#expected_bo+expected_tx+expected_col)
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
	return time


'''def drawNetwork(nodes):
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
	plt.show()'''

if __name__ == "__main__":
	nNodes = int(sys.argv[1])
	nBeams = int(sys.argv[2])
        nodes = []
        latitude=10
        longitude = 10
        leader = 0#int(sys.argv[1])
        #chosen = int (sys.argv[2])
        seed = int(sys.argv[6])#5])
	relief = int(sys.argv[5])
        random.seed(seed)

	mmw_rate=25.8
	legacy_rate=1.0

	#==================================
	#	TIME DEFINITIONS
	#
	# time unit -> micro seconds
	#==================================
	time_arr = {'sswack':31/mmw_rate,
			'ack':31/legacy_rate,
			'ssw':26/mmw_rate,#bytes/transmission_rate
			'sswfeedback':31/mmw_rate,
		    	'acktimeout':300,
			'txData':(1024+34+16)*8/mmw_rate,
			'txMap':(16+34+(nNodes*50))*8/legacy_rate,#to do: define the length of map packet
			'txRts':20.0*8/legacy_rate,#bytes*8/transmission_rate(Mbps)
			'txCts':14.0*8/legacy_rate,#bytes*8/transmission_rate(Mbps)
			'txNum':(34+16+(nNodes*50))*8/legacy_rate,#to do: define the length of ranking packet
			'sifs':28,
			'mmwsifs':3,
			'difs':128,
			'sbifs':1}
	

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


	#======================================
	#	CREATING NODES
	#
	# leader created at the centre of net
	#======================================
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

	num = 0 # Number of correct estimatives
	den = 0 # Number of all estimatives

	#drawNetwork(nodes)

	#=====================================
	#     CREATING NODES' ANGLE LIST
	#=====================================
	#proof = [] #list to save the correct beamforming and compare with proposed algorithm
	for i in range(nNodes):
		nodes[leader].angleList.append(beamformingReal(nodes,leader,i,'normal','normal', mu_d, sigma_d, mu_a, sigma_a))
	#print nodes[leader].angleList

	#========================================
	#   CHECKING THE ERRORS IN ESTIMATING
	#========================================
	proof=[] #this array stores the correct angles
	fair=[]
	ang_err = 0
	averageBeamError=0
	count=0
	for j in range(nNodes):
		hitsOnTarget = 0
		temp = []
		chosen = j
		for i in range(nNodes):
			### --------------------------------ESTIMATING ANGLES---------------------------------------
			nodes[chosen].angleList.append(estimating(nodes,chosen, i, leader, nodes[leader].angleList))
			temp.append(beamforming(nodes,chosen,i))
		proof.append(temp)

		template = "{0:15}"
		for i in range(nNodes):
			den = den + 1
			#print template.format(proof[i]),
			#print template.format(nodes[chosen].angleList[i]),
			if relief == 0: # This IF statement defines if one beam error will be considered
				if temp[i][0] <> nodes[chosen].angleList[i][0]:
					#=========== uncomment below for log =============
					#
					#print chosen, i, "--->",
					#print template.format(temp[i]),
                                	#print template.format(nodes[chosen].angleList[i])
					#
					#==================================================
					ang_err = ang_err + abs(temp[i][2] - nodes[chosen].angleList[i][2])
					num = num + 1
					hitsOnTarget += 1
				else: #count the average error when some node is rigth
					averageBeamError += abs(temp[i][2] - nodes[chosen].angleList[i][2])
					count+=1
			else:
				if abs(temp[i][0] - nodes[chosen].angleList[i][0])>1:
					if not ((temp[i][0]==0 and nodes[chosen].angleList[i][0]==nodes[chosen].nBeams-1)
					or (temp[i][0]==nodes[chosen].nBeams-1 and nodes[chosen].angleList[i][0]==0)):
						#============ uncomment below for log ============
						#
						#print chosen, i, "--->",
						#print template.format(temp[i]),
						#print template.format(nodes[chosen].angleList[i])
						#
						#=================================================
						ang_err = ang_err + abs(temp[i][2] - nodes[chosen].angleList[i][2])
						num = num + 1
						hitsOnTarget +=1
					else:
						averageBeamError += abs(temp[i][2] - nodes[chosen].angleList[i][2])
						count+=1

				else:
					averageBeamError += abs(temp[i][2] - nodes[chosen].angleList[i][2])
					count+=1
		fair.append(hitsOnTarget)

	part = 0
	#PRIMARY MATCHING RATE
	print 1.0 - round(1.0*num/den,6)

	#for i in fair: part += i**2
	#fairness = 1.0*sum(fair)**2/(nNodes*part)
				#print template.format(proof[i]),
				#print template.format(nodes[chosen].angleList[i]),
				#print "-----> ERROR sectorized2.py", leader, chosen, seed
			#else: print "\n",'''

	#print "Number of wrong angles", round(1.0*num/den,6)#number of errors

	#UNCOMMENT THIS LATER!!!
	#
	#if num <> 0: print round(1.0*ang_err/num, 6)#average erro in radians
	#else: print 0.0
	#print round(1.0*b/count,6)

	#print round(fairness,6)
	#fair = range(nNodes)

	#===============================================
	#     FIRST PROPOSED WORK TIME CALCULATION
	#===============================================
	for i in fair: fair[i]=0
	num = 0
	den = 0
	# Time taken to beamforming with LEADER
	t_beamforming = ((time_arr['ssw']*nBeams)+(time_arr['sbifs']*(nBeams-1))+(2*time_arr['sifs'])+time_arr['sswfeedback']+time_arr['sswack'])
	# Time taken in OVERHEAD transmiting map and etc
	bf_mundi = (nNodes*2*t_beamforming)+((nNodes-1)*time_arr['sifs'])
	ctrl_mundi = time_arr['txNum']+(nNodes-1)*(time_arr['sifs']+time_arr['txMap'])
	schedule = txSched(nodes,nNodes)
	overhead = 0
	#print schedule
	for i in schedule:
		overhead += time_arr['difs']+time_arr['txRts']+time_arr['sifs']+time_arr['txCts']+time_arr['sifs']
		#print i[0], nodes[i[0]].x, nodes[i[0]].y, '|', i[1], nodes[i[1]].x,nodes[i[1]].y, nodes[i[0]].angleList[i[1]][0]
		den += 1
		numberOfRetrials, time = txCheck(nodes,proof,i[0],i[1], time_arr)
		overhead += time
		#fair[i[0]]+=a
		num += numberOfRetrials

	#print "Average number of transmission retrials", round(1.0*num/den,6), "(due to angle missmatch)"
	#print "Number of transmissions scheduled", len(schedule)
	#print "Overhead caused by algorithm", overhead
	part = 0

	#for i in fair: part += i**2
	#fairness = 1.0*sum(fair)**2/(nNodes*part)

	#overhead is not exactly the overhead, but the time taken to run all protocol stages
	mundimapp = overhead
 	#print mundimapp
        print overhead/1e6
        print bf_mundi/1e6
        print ctrl_mundi/1e6
        print overhead/1e6 + bf_mundi/1e6 + ctrl_mundi/1e6


	#================================================
	#     SECOND PROPOSED WORK TIME CALCULATION
	#================================================
	# 	Calculation of overheard nodes
	bf_go = (nNodes*4*t_beamforming) + (nNodes*time_arr['sifs'])
	ctrl_go = time_arr['txNum']+time_arr['sifs']
	overheard = []
	maximo = 0
	for i in nodes:
		if i.isLeader == True: continue
		#print i.Id
		overheard.append([])
		#print overheard
		if maximo < count: maximo = count
		count = 0
		while len(overheard[i.Id-1])<>(nNodes-1):
			count+=1
			for j in nodes:
				if i.Id <> j.Id:
					ov = overhear(i,j)
					#print ov
					if ov <> 1 and not j.Id in overheard[i.Id-1]: 
						overheard[i.Id-1].append(j.Id)#count += 1
						#print overhear(i,j)
		#overheard.append(count)
		#print overheard
	#print overheard
	#print "maximo de rodadas de overhear", maximo

	#	Calculation of time to transmit in wifi band
	cw_min = 15
	slot = ((time_arr['difs']-time_arr['sifs'])/2)
	slrc = 7
	feedbackLength = 60
	accessTime = wifiModel(cw_min, nNodes-1,time_arr['difs'], time_arr['sifs'],
			     feedbackLength,time_arr['ack'], time_arr['acktimeout'], slot, slrc, legacy_rate )

	#gomundi_time += accessTime + time
	ctrl_go += accessTime
	print ctrl_go/1e6
	print bf_go/1e6
	overhead = 0
        for i in schedule:
                overhead += time_arr['difs']+time_arr['txRts']+time_arr['sifs']+time_arr['txCts']+time_arr['sifs']
		overhead += time_arr['txData']+time_arr['sifs']+time_arr['ack']
	print overhead/1e6

	#================================================
	#	     MDND TIME CALCULATION
	#================================================
	mdnd={'probereq':(1024+34+16)*8/legacy_rate,
		'proberesp':32*8/legacy_rate,
		'addtsreq':(1024+34+16)*8/legacy_rate,
		'addtsresp':32*8/legacy_rate,
		'chreq':(1024+34+16)*8/legacy_rate,
		'chresp':32*8/legacy_rate,
		'xchreq':(1024+34+16)*8/legacy_rate,
		'xchresp':32*8/legacy_rate,
		'ssw':time_arr['ssw'],
		'sswfeedback':time_arr['sswfeedback'],
		'sswack':time_arr['sswack'],
		'disconn':(1024+34+16)*8/legacy_rate}

	past_nodes = []
	ctrl_mdnd = 0
	bf_mdnd = 0
	overhead=0
	for i in schedule:
		if past_nodes.count(i[0])==0:
			past_nodes.append(i[0])
			ctrl_mdnd += mdnd['probereq']+time_arr['sifs']+mdnd['proberesp']
		if schedule.index(i) < schedule.index([i[1],i[0]]):
			bf_mdnd += 2*((mdnd['ssw']*nBeams)+(time_arr['sbifs']*(nBeams-1))+(2*time_arr['sifs'])+mdnd['sswfeedback']+mdnd['sswack'])

		ctrl_mdnd += mdnd['addtsreq']+time_arr['sifs']+mdnd['addtsresp']+time_arr['sifs'] 
		ctrl_mdnd += 2*(mdnd['chreq']+time_arr['sifs']+mdnd['chresp']+time_arr['sifs']) 
		ctrl_mdnd += 2*(mdnd['xchreq']+time_arr['sifs']+mdnd['xchresp']+time_arr['sifs'])
		overhead += time_arr['txData']+time_arr['sifs']+time_arr['ack']+time_arr['sifs']
		ctrl_mdnd += (4*accessTime) + mdnd['disconn']
	print ctrl_mdnd/1e6
	print bf_mdnd/1e6
	print overhead/1e6
