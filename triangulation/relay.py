import math
import random
import sys
import Nodes
import scheduler
import Beamforming


pi = math.pi


'''def centroidReal(nodes):
	x = []
	y = [] 
	coord = []
	for i in nodes[leader].angleList:
		#coord.append([math.cos(i[2])*i[1], math.sin(i[2])*i[1]])
		x.append(math.cos(i[2])*i[1])
		y.append(math.sin(i[2])*i[1])

	cx = sum(x)/len(nodes[leader].angleList)
	cy = sum(y)/len(nodes[leader].angleList)
	print cx, cy'''

	

def headElection(nodes, nNodes, cluster):
	#achar o mais proximo do centroide da rede
	if len(cluster)==0:
		return None
	coord = []
	minimum = nodes[leader].angleList[cluster[0]][1]
	head = cluster[0]
	for i in cluster:
		#coord.append([math.cos(nodes[leader].angleList[i][2])*nodes[leader].angleList[i][1],
		#	      math.sin(nodes[leader].angleList[i][2])*nodes[leader].angleList[i][1]])
		if minimum > nodes[leader].angleList[i][1]:
			head = i
	return head
	
def clusterFormation(nodes, nNodes, nClusters, leader):
	coord = []
	lim = int(nodes[leader].nBeams/nClusters)#2.0*pi/nClusters #int(nodes[leader].nBeams/nClusters)
	for i in range(nClusters):
		coord.append([])
	count = 0
	for i in nodes[leader].angleList:
		#print lim, i[0], math.degrees(i[2]), int(i[0]/lim)
		#print count
		if i == [0,0,0]: 
			coord[0].append(leader)
		else:
			#coord.append([math.cos(i[2])*i[1], math.sin(i[2])*i[1]])
			coord[int(i[0]/lim)].append(count)
		count += 1
	#print coord
	heads = []
	for i in range(nClusters):
		heads.append(headElection(nodes, nNodes, coord[i]))
		
	coord.append(heads)
	return coord


def quicksort(array, arrayMap, first, last):
	if len(array) <> len(arrayMap):
		print "Array length does not Match"
		return -1
	
	if first < last:
		splitpoint = partition(array, arrayMap, first, last)
		quicksort(array, arrayMap, first, splitpoint-1)
		quicksort(array, arrayMap, splitpoint+1, last)

def partition(array, arrayMap, first, last):
	pivot = array[first]
	pivotMap = arrayMap[first]

	leftmark = first+1
	rightmark = last
	done = False
	while not done:
		while leftmark <= rightmark and array[leftmark] <= pivot:
			leftmark += 1
		while rightmark >= leftmark and array[rightmark] >= pivot:
			rightmark -= 1
		if rightmark < leftmark:
			done = True
		else:
           		temp = array[leftmark]
           		array[leftmark] = array[rightmark]
           		array[rightmark] = temp
			temp = arrayMap[leftmark]
			arrayMap[leftmark] = arrayMap[rightmark]
			arrayMap[rightmark] = temp

	temp = pivot
	array[first] = array[rightmark]
	arrayMap[first]=arrayMap[rightmark]
	array[rightmark] = temp
	arrayMap[rightmark] = pivotMap

	return rightmark


def mean(array):
	mean = 0
	for i in array:
		mean += i
	mean = mean/len(array)

def median(data):
    new_list = sorted(data)
    if len(new_list)%2 > 0:
        return new_list[len(new_list)/2]
    elif len(new_list)%2 == 0:
        return (new_list[(len(new_list)/2)] + new_list[(len(new_list)/2)-1]) /2.0

def anotherClusterFormation(nodes, nNodes, nClusters, leader):
	clusters = []
	heads = []
	distMap = []
	matrix = []
	lim = int(nNodes/nClusters)
	for i in range(nClusters): clusters.append([])
	#for i in range(nNodes): 
	#	copy.append(i)
	#	matrix.append([])
	#every cluster will have the same length
	for i in range(nNodes):
		for j in range(nNodes):
			if i == j:
				pass
			else:
				ix = math.cos(nodes[leader].angleList[i][2])*nodes[leader].angleList[i][1]
				iy = math.sin(nodes[leader].angleList[i][2])*nodes[leader].angleList[i][1]
				jx = math.cos(nodes[leader].angleList[j][2])*nodes[leader].angleList[j][1]
				jy = math.sin(nodes[leader].angleList[j][2])*nodes[leader].angleList[j][1]
				matrix.append(math.hypot(abs(ix-jx),abs(iy-jy)))
				distMap.append([i,j])
	#print matrix, distMap
	quicksort(matrix, distMap, 0, len(matrix)-1)
	#print distMap 
	cut = median(matrix)
	mins = []
	for i in range(nNodes):
		count = 0
		for j in distMap:
			if j[0] == i:
				count += distMap.index(j)
		mins.append(count)
	#print mins
	count = 0
	while len(heads)<>nClusters:
		att = min(mins)
		heads.append(mins.index(att))
		#mins.remove(att)
		mins[mins.index(att)]=1e9
		#count+=1
	#print clusters 
	clusters.append(heads)
	#print clusters
	for i in range(lim):
		for j in heads:#clusters:
			for k in distMap:
				check = 0
				if j==k[0] and len(clusters[heads.index(j)])<=lim:
					for l in clusters: 
						if l.count(k[1])<>0:
							check+=1
					if check==0:
						clusters[heads.index(j)].append(k[1])
						break
	#print clusters
	return clusters


def wifiModel(nNodes, slrc, cwMin,cwMax, tAck, tSifs, tDifs, timeOut, tSlot, tData):
	#expected time to one node transmit between nNodes contending for the medium
        tau = 0
        expectedR = 0
        for m in range(1,slrc):
                collisions = 1
                for k in range(m-1):
                        if ((2.0**k)*cwMin) <= cwMax:
                                tau = 2.0/((2.0**k)*cwMin+1)
                        else:
                                tau = 2.0/(cwMax + 1)
                        num = nNodes*tau*(1.0 -tau)**(nNodes-1)
                        den = 1.0 - (1.0 -tau)**nNodes
                        collisions = collisions*(1.0 - num/den)

                if ((2.0**m)*cwMin) <= cwMax:
                        tau = 2.0/((2.0**(m-1))*cwMin+1)
                else:
                        tau = 2.0/(cwMax +1)
                num = tau*(1-tau)**(nNodes-1)
                den = 1 - (1 - tau)**nNodes
                expectedR += nNodes*(num/den)*collisions*m

        r = int(math.ceil(expectedR))
        txTime = 0
        for i in range(r):
                #txTime += ((2**i)*cwMin/2)*tSlot
                txTime += (1.0/((2**i)*cwMin))*tSlot

        #txTime += tDifs + (r)*(tSifs+tData) + ((r-1)*timeOut) + (tSifs+tAck)
        txTime += tDifs + (r+1)*(tSifs+tData+tAck)

        return txTime, r


		
if __name__ == "__main__":
	latitude = 10
	longitude = 10
	sense = 20
	mmw_rate = 1
	legacy_rate = 1

	nNodes = int(sys.argv[1])
	nBeams = int(sys.argv[2])
	relief = int(sys.argv[6])
	seed = int(sys.argv[7])
	leader = 0
	random.seed(seed)


	nodes = Nodes.createNet(latitude, longitude, sense, nNodes, nBeams,leader)



	
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
        indexd = 2#int(sys.argv[3])
        indexa = 2#int(sys.argv[4])

        #==== DEFINING ARRAYS ====#
        meand = [-1, 0.1,0.2,0.3,0.4,0.5,0.6]
        devd = [-1, 1.0,1.2,1.4,1.6,1.8,2.0]
        deva = [-1, 5, 10, 15, 20]

        #==== GETTING VALUES ====#
        mu_d = meand[indexd]
        sigma_d = devd[indexd]
        mu_a = 0 #meana[indexa]
        sigma_a = deva[indexa]
		
	#CREATING LEADER 
	for i in range(nNodes):
                nodes[leader].angleList.append(Beamforming.beamformingReal(nodes,leader,i,
						'normal','normal', mu_d, sigma_d,mu_a, sigma_a))
	proof = []
	erros = Beamforming.mapCheck(nodes, nNodes, leader, relief, proof)
	#print erros[0]*1.0/erros[1]

	for i in range(nNodes):
		Nodes.setRelays(nodes[i], nNodes)


	num = 0
	den = 0
	nPeople = int(sys.argv[3])
	vPeople = float(sys.argv[4]) #meters per second
	rate = float(sys.argv[5])
	peopleArr = scheduler.peopleOrigin(nPeople, latitude, longitude)
        t_beamforming = ((time_arr['ssw']*nBeams)+(time_arr['sbifs']*(nBeams-1))+(2*time_arr['sifs'])+time_arr['sswfeedback']+time_arr['sswack'])
        # Time taken in OVERHEAD transmiting map and etc
        bf_mundi = (nNodes*2*t_beamforming)+((nNodes-1)*time_arr['sifs'])
	ctrl_mundi = time_arr['txNum']+(nNodes-1)*(time_arr['sifs']+time_arr['txMap'])
        schedule = scheduler.txSched(nodes,nNodes,rate)
        #print schedule
	Time = 0
	overhead = 0
	retrying = 0
	blocked = 0
	relayed = 0
	transmited = 0
	discarded = 0
        for i in schedule:
		for j in range(int(i[2])):
			overhead += time_arr['difs']+time_arr['txRts']+time_arr['sifs']+time_arr['txCts']+time_arr['sifs']
			den += 1
			#numberOfRetrials, time = scheduler.txCheck(nodes,proof,i[0],i[1], time_arr, relief)
			numberOfRetrials, timea, time, timeb, timeR, check = scheduler.relayCheck(peopleArr, vPeople, nodes, proof, i[0], i[1], time_arr, relief, overhead/1e6, latitude, longitude)
			overhead += time + timea + timeb + timeR
			#Time += time + timea + timeb + timeR
			blocked += timeb
			retrying += time
			relayed += timeR
			transmited += timea 
			#fair[i[0]]+=a
			num += numberOfRetrials
			if check == False: discarded += 1

        #print "Average number of transmission retrials", round(1.0*num/den,6), "(due to angle missmatch)"
        #print "Number of transmissions scheduled", len(schedule)
        #print "Overhead caused by algorithm", overhead
        #overhead is not exactly the overhead, but the time taken to run all protocol stages
        mundimapp = overhead
        #print mundimapp/1e6
	print overhead/1e6
	print bf_mundi/1e6
	print ctrl_mundi/1e6
	print overhead/1e6 + bf_mundi/1e6 + ctrl_mundi/1e6
	print transmited/1e6
	print blocked/1e6
	print retrying/1e6
	print relayed/1e6
	print 100 - 100*(1.0*discarded/len(schedule))


	
	##################################################
	#
	#		CLUSTER PROTOCOL
	#
	##################################################
	nClusters = 3#4
	#clusters = clusterFormation(nodes,nNodes,nClusters,leader)
	#print clusters
	clusters = anotherClusterFormation(nodes,nNodes,nClusters,leader)
	#print clusters

	#CLEANING ANGLE LIST
	for i in nodes:
		i.angleList = []
		for j in range(nNodes): i.angleList.append([])

	count = 0
	#FULLFILING ANGLELIST WITH BEAMFORMING AMONG HEADS AND CLUSTER MEMBERS
	for i in clusters[nClusters]:
		if i == None:
			pass
		else:
			for j in clusters[count]:
				nodes[i].angleList[j] = Beamforming.beamformingReal(nodes,i,j,
							'normal','normal', mu_d, sigma_d,mu_a, sigma_a)
			for j in clusters[nClusters]:
				if j == None:
					pass
				else:
					nodes[i].angleList[j] = Beamforming.beamformingReal(nodes,i,j,
							'normal','normal', mu_d, sigma_d,mu_a, sigma_a)
		count+=1
		#print nodes[i].angleList

	#COMPLETING ANGLE LIST RECALCULATING THE MAPS FROM OTHERS HEADS
	for i in clusters[nClusters]:
		for j in clusters[nClusters]:
			'''nodes[i].angleList[j] = Beamforming.beamformingReal(nodes,i,j,
                                                'normal','normal', mu_d, sigma_d,mu_a, sigma_a)'''
			if j <> i and j <> None and i<> None:
				#count = 0
				count = clusters[nClusters].index(j)
				#while clusters[count].count(j)==0: count+=1
				for n in clusters[count]:
					#print n, i, j
					#print nodes[j].angleList[i]
					#print nodes[j].angleList[n]
					
					nodes[i].angleList[n] = Beamforming.estimating(nodes, i, n, j, nodes[j].angleList)
		#print nodes[i].angleList

	for i in range(nClusters):
		pleader = clusters[nClusters][i]
		proof = []
		temp = []
		for j in clusters[i]:
			for n in range(nNodes):
				if n <> j:
					#print n, j, pleader
                                        #print nodes[pleader].angleList[j]
                                        #print nodes[pleader].angleList[n]
					nodes[j].angleList[n] = Beamforming.estimating(nodes, j, n, pleader, nodes[pleader].angleList )
	erro=0
	proof = []
	for i in range(nNodes):
		proof.append([])
		#print nodes[i].angleList
		for j in range(nNodes):
			temp =[]
			proof[i].append([])
			if i <> j:
				temp = Beamforming.beamforming(nodes, i, j)
				proof[i][j] = temp
				if temp[0] <> nodes[i].angleList[j][0] and relief == 0:
					erro+=1
				elif relief == 1 and (temp[0]<>nodes[i].angleList[j][0]+1 or temp[0]<>nodes[i].angleList[j][0]-1):
					erro+=1
	#print erro*1.0/erros[1]
	
	maxCluster = len(clusters[0])
	for i in range(nClusters):
		test = len(clusters[i])
		if test > maxCluster: maxCluster = test

	#print maxCluster

	time = 0
	r = 0
	s = 1024
	txRate = 6
	cwMin = 7
	#cwMax = 4095
	slrc = int(math.log(1.0*s, 2) - math.log(1.0*cwMin, 2))
	tAck =  40.6901 ### 32.0*8.0/txRate
	tSifs = 10
	tSlot = 9
	tDifs = (2*tSlot) + tSifs
	timeOut = 75
	tData = 76.2939# us  ###60*8.0/txRate
	time, r = wifiModel(n, slrc, cwMin,s, tAck, tSifs, tDifs, timeOut, tSlot, tData)
	totalTime = 0
	transient = 0
	a = 0
	#time,r = wifiModel(nClusters, slrc, cwMin,s, tAck, tSifs, tDifs, timeOut, tSlot, tData)
	time,r = wifiModel((nNodes/nClusters), slrc, cwMin,s, tAck, tSifs, tDifs, timeOut, tSlot, tData)
	map_cluster = time*(nNodes/nClusters - 1)#(maxCluster-1)
	'''for i in range(1,nClusters):
		transient, r = wifiModel(nClusters, slrc, cwMin,s, tAck, tSifs, tDifs, timeOut, tSlot, tData)	
		map_cluster += transient'''
	#map_cluster += (nClusters - 1)*time_arr['sifs']
	map_cluster += (nNodes/nClusters - 1)*time_arr['sifs']
	maxCluster = int(nNodes/nClusters)
	bf_cluster = t_beamforming*(maxCluster*2 + nClusters*2)
	ctrl_cluster = time_arr['sifs']+ time_arr['txNum']+time_arr['sifs'] #+time_arr['txMap']*nClusters
	overhead = 0
	for i in schedule:
		overhead += time_arr['difs']+time_arr['txRts']+time_arr['sifs']+time_arr['txCts']+time_arr['sifs']
                den += 1
                numberOfRetrials, time = scheduler.txCheck(nodes,proof,i[0],i[1], time_arr, relief)
                overhead += time
                num += numberOfRetrials
	'''print overhead/1e6
	print bf_cluster/1e6
	print ctrl_cluster/1e6
	print map_cluster/1e6
	print overhead/len(schedule)/1e6'''

