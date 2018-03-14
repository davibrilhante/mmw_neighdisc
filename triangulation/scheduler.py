import math
import random
import Nodes
from time import sleep

pi = math.pi


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





def txCheck(nodes, proof, tx, rx, tdict, relief):
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
                elif relief==1 and abs(nodes[tx].angleList[rx][0] - proof[tx][rx][0]) <= 1:
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

def peopleOrigin(nPeople, latitude, longitude):
	peopleArr = []
	#Setting the origin of humans
	for i in range(nPeople): peopleArr.append([random.randint((-latitude/2.0),(latitude/2.0)),random.randint((-longitude/2.0),(longitude/2.0)),random.uniform(0,2*pi)])
	return peopleArr

def peopleMovement(vPeople, peopleArr, timePast, timeNow, latitude, longitude):
	interval = timeNow - timePast
	space = interval*vPeople
	for i in peopleArr:
		#angle = math.radians(random.choice([0,45,90,135,180]))#random.randint(0,180))
		changeDirection = random.randint(1,10)
		if changeDirection >= 10: i[2] = random.uniform(0,pi)
		angle = i[2]
		i[0] += space*math.cos(angle)
		i[1] += space*math.sin(angle)
		while (i[0] < -latitude/2  or i[0] > latitude/2) or (i[1] < -longitude/2 or i[1] > longitude/2):
			#print "tem um loopzinho aqui"
			i[0] -= space*math.cos(angle)
			i[1] -= space*math.sin(angle)
			angle = math.radians(random.randint(0,360))
			i[2] = angle
			i[0] += space*math.cos(angle)
                	i[1] += space*math.sin(angle)


def projections(r,node, adj, beam):
        precision = 3
        Projection = []
        alpha = 2*pi/node.nBeams
	n = beam
        #for n in range(node.nBeams):
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

	#Projection.append([[round(x1,precision),round(x2,precision)],
	#		   [round(y1,precision),round(y2,precision)]])
	Projection = [[round(x1,precision),round(x2,precision)],
                      [round(y1,precision),round(y2,precision)]]
	#print "[",x1,",",x2,"] [",y1,",",y2,"]"
        return Projection


def blockage(i, j, ri, rj, peopleArr, rPeople):
        theta1 = math.atan2(j.y-i.y,j.x-i.x)
        theta2 = math.atan2(i.y-j.y,i.x-j.x)
        if theta1 < 0: theta1 = 2*pi + theta1
        if theta2 < 0: theta2 = 2*pi + theta2

        #print math.degrees(theta1), math.degrees(theta2)
        d = math.hypot(i.x-j.x, i.y-j.y)
        delta = 0.25*(math.sqrt((d+ri+rj)*(d+ri-rj)*(d-ri+rj)*(-d+ri+rj)))
	#Obtaining the coordinates of intersection points between the two circles
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

        newI = Nodes.Node(distI*math.cos(deltaI), distI*math.sin(deltaI), 10)
        newJ = Nodes.Node(distJ*math.cos(deltaJ), distJ*math.sin(deltaJ), 10)
        newI.setBeams(i.nBeams)
        newJ.setBeams(j.nBeams) #to receiver we will set the quasi omni mode

        projectionsI = projections(d, newI, theta1, i.angleList[j.Id][0])
        projectionsJ = projections(d, newJ, theta1, j.angleList[i.Id][0])

	x_int = [min(projectionsI[0][0], projectionsJ[0][0]),max(projectionsI[0][1], projectionsJ[0][1])]
	y_int = [min(projectionsI[1][0], projectionsJ[1][0]),max(projectionsI[1][1], projectionsJ[1][1])]

	for i in peopleArr:
		distPeople = math.hypot(i[0]-x2, i[1]-y2)
		deltaPeople = math.atan2(i[1]-y2,i[0]-x2) - theta1

		xPeople = distPeople*math.cos(deltaPeople)
		yPeople = distPeople*math.sin(deltaPeople)

		xProjPeople = [xPeople - rPeople,xPeople + rPeople]
		yProjPeople = [yPeople - rPeople,yPeople + rPeople]

		if xProjPeople[0] < x_int[0] and xProjPeople[1] > x_int[1]: 
			#print "Blocked in X by Person", peopleArr.index(i), i
			return True
		'''elif (xProjPeople[0] < x_int[0] and xProjPeople[1] < x_int[1]) and xProjPeople[1] - x_int[0] >= 0.6*(x_int[1]-x_int[0]):
			return True
		elif (xProjPeople[0] > x_int[0] and xProjPeople[1] > x_int[1]) and xProjPeople[0] - x_int[1] >= 0.6*(x_int[1]-x_int[0]):
			return True
		elif (xProjPeople[0] > x_int[0] and xProjPeople[1] < x_int[1]) and xProjPeople[0] - x_int[1] >= 0.6*(x_int[1]-x_int[0]):
			return True'''
		if yProjPeople[0] < y_int[0] and yProjPeople[1] > y_int[1]: 
			#print "Blocked in Y by Person", peopleArr.index(i), i
			return True
		'''elif (yProjPeople[0] < y_int[0] and yProjPeople[1] < y_int[1]) and yProjPeople[1] - y_int[0] >= 0.6*(y_int[1]-y_int[0]):
			return True
		elif (yProjPeople[0] > y_int[0] and yProjPeople[1] > y_int[1]) and yProjPeople[0] - y_int[1] >= 0.6*(y_int[1]-y_int[0]):
			return True
		elif (yProjPeople[0] > y_int[0] and yProjPeople[1] < y_int[1]) and yProjPeople[0] - y_int[1] >= 0.6*(y_int[1]-y_int[0]):
			return True'''

	return False

def movingTxCheck(peopleArr, vPeople, nodes, proof, tx, rx, tdict, relief, Time, lat, lont):
	time = 0
	timeb = 0
	timea = 0
	temp = Time
        check = False
        i = 1
        signal = random.choice([-1,1])
        #attempt = random.choice([-1,1])
        while  check == False:
		#print temp, peopleArr #"Loop Infinito aqui: schedule.py line 225"
		#sleep(0.3)
                #if i <> 1:
                attempt = -1*signal*i
                signal = signal*-1
		peopleMovement(vPeople, peopleArr, temp/1e6, (Time + timea + timeb + time)/1e6, lat, lont)
		temp = Time + timea + timeb + time
                #print attempt, i
                #raw_input()
		if not blockage(nodes[tx], nodes[rx], 10,10 ,peopleArr, 0.3):
		#the sector obtained from lider is ok!
			if nodes[tx].angleList[rx][0] == proof[tx][rx][0]:
				timea += tdict['txData']+tdict['mmwsifs']
				#print "Enviou com sucesso"
				check =True
		#The sector obtained is not ok, but we will alleviate
			elif relief==1 and abs(nodes[tx].angleList[rx][0] - proof[tx][rx][0]) <= 1:
				timea += tdict['txData']+tdict['mmwsifs']
				check =True
		#The sector is not ok and we will guess another adjacent sector
			else:
				nodes[tx].angleList[rx][0] += attempt
				if nodes[tx].angleList[rx][0] < 0: nodes[tx].angleList[rx][0] = nodes[tx].nBeams + nodes[tx].angleList[rx][0]
				elif nodes[tx].angleList[rx][0] > nodes[tx].nBeams -1:
					nodes[tx].angleList[rx][0] = nodes[tx].angleList[rx][0] - nodes[tx].nBeams
				time += tdict['txData']+tdict['acktimeout']
				i += 1
		else:
			nodes[tx].angleList[rx][0] += attempt
			if nodes[tx].angleList[rx][0] < 0: nodes[tx].angleList[rx][0] = nodes[tx].nBeams + nodes[tx].angleList[rx][0]
			elif nodes[tx].angleList[rx][0] > nodes[tx].nBeams -1:
				nodes[tx].angleList[rx][0] = nodes[tx].angleList[rx][0] - nodes[tx].nBeams
			timeb += tdict['txData']+tdict['acktimeout']
			i += 1	
		if i == 32: break
        timea += tdict['ack']
        # Returns the time spent to transmit the information, 
        # taking in count the possible retransmissions and the 
        # time to find the right beam to neighbor
	#timea: time spent in a transmission without error
	#time: time spent in retries
	#timeb: time spent in blockage
        return [i, timea, time, timeb, check]


def relayCheck(peopleArr, vPeople, nodes, proof, tx, rx, tdict, relief, Time, lat, lont):
	time = 0
	timeb = 0
	timea = 0
	timeR = 0
	temp = Time
        check = False
        i = 1
        signal = random.choice([-1,1])
        #attempt = random.choice([-1,1])
	relay = nodes[tx].relays[rx]
        while  check == False:
		if i == 32: break

		###print "Relay de", tx, "para", relay, "para", rx
                attempt = -1*signal*i
                signal = signal*-1
		peopleMovement(vPeople, peopleArr, temp/1e6, (Time + timea + timeb + time)/1e6, lat, lont)
		temp = Time + timea + timeb + time
		if not blockage(nodes[tx], nodes[rx], 10,10 ,peopleArr, 0.3):

		#the sector obtained from lider is ok!
			if nodes[tx].angleList[rx][0] == proof[tx][rx][0]:
				timea += tdict['txData']+tdict['mmwsifs']
				check =True

		#The sector obtained is not ok, but we will alleviate
			elif relief==1 and abs(nodes[tx].angleList[rx][0] - proof[tx][rx][0]) <= 1:
				timea += tdict['txData']+tdict['mmwsifs']
				check =True

		#The sector is not ok and we will guess another adjacent sector
			else:
				nodes[tx].angleList[rx][0] += attempt
				if nodes[tx].angleList[rx][0] < 0: nodes[tx].angleList[rx][0] = nodes[tx].nBeams + nodes[tx].angleList[rx][0]
				elif nodes[tx].angleList[rx][0] > nodes[tx].nBeams -1:
					nodes[tx].angleList[rx][0] = nodes[tx].angleList[rx][0] - nodes[tx].nBeams
				time += tdict['txData']+tdict['acktimeout']
				i += 1
				#Volta no While

		#vai fazer relay
		elif not blockage(nodes[tx], nodes[relay], 10,10 ,peopleArr, 0.3) and not blockage(nodes[relay],nodes[rx], 10,10 ,peopleArr, 0.3):
				"""
				print "Relay de", tx, "para", relay, "para", rx
				print nodes[tx].angleList[relay]
				print proof[tx][relay]
				print nodes[relay].angleList[rx]
				print proof[relay][rx]
				sleep(0.1)#"""
				if nodes[tx].angleList[relay][0] == proof[tx][relay][0]:
                                	timeR += tdict['txData']+tdict['mmwsifs']
					if nodes[relay].angleList[rx][0] == proof[relay][rx][0]:
                                        	timeR += tdict['txData']+tdict['mmwsifs']
                                        	check =True
					else:
						#O angulo do relay para o RX esta incorreto
						###print "attempt", attempt
		                                nodes[relay].angleList[rx][0] += attempt
                               			if nodes[relay].angleList[rx][0] < 0: nodes[relay].angleList[rx][0] = nodes[relay].nBeams + nodes[relay].angleList[rx][0]
                                		elif nodes[relay].angleList[rx][0] > nodes[relay].nBeams -1:
                                        		nodes[relay].angleList[rx][0] = nodes[relay].angleList[rx][0] - nodes[relay].nBeams
                                		time += tdict['txData']+tdict['acktimeout']
                                		i += 1
                                		#Volta no While

				else:
					#O angulo do tx para o relay esta incorreto
	                                nodes[tx].angleList[relay][0] += attempt
					if nodes[tx].angleList[relay][0] < 0: nodes[tx].angleList[relay][0] = nodes[tx].nBeams + nodes[tx].angleList[relay][0]
					elif nodes[tx].angleList[relay][0] > nodes[tx].nBeams -1:
						nodes[tx].angleList[relay][0] = nodes[tx].angleList[relay][0] - nodes[tx].nBeams
					time += tdict['txData']+tdict['acktimeout']
					i += 1
					#Volta no While


		#Vai tentar retransmitir
		else:
			nodes[tx].angleList[rx][0] += attempt
			if nodes[tx].angleList[rx][0] < 0: nodes[tx].angleList[rx][0] = nodes[tx].nBeams + nodes[tx].angleList[rx][0]
			elif nodes[tx].angleList[rx][0] > nodes[tx].nBeams -1:
				nodes[tx].angleList[rx][0] = nodes[tx].angleList[rx][0] - nodes[tx].nBeams
			timeb += tdict['txData']+tdict['acktimeout']
			i += 1	
			#Volta no While

        timea += tdict['ack']


        # Returns the time spent to transmit the information, 
        # taking in count the possible retransmissions and the 
        # time to find the right beam to neighbor
	#timea: time spent in a transmission without error
	#time: time spent in retries
	#timeb: time spent in blockage
	#timeR: time on relays
        return [i, timea, time, timeb, timeR, check]
