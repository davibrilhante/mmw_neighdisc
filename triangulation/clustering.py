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

def anotherClusterFormation(nodes, nNodes, nClusters, leader):
	clusters = []
	copy = []
	matrix = []
	lim = int(nNodes/nClusters)
	for i in range(nClusters): clusters.append([])
	for i in range(nNodes): 
		copy.append(i)
		matrix.append([])
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
	for i in matrix:
		clustered = False
		while clustered == False:
			ideal = i.index(min(i))
			for j in clusters:
				if j.count(ideal)<>0 and len(j)<lim:
					j.append(i)
					clustered = True
					break
			if clustered == False:
				i.pop(ideal)
if __name__ == "__main__":
	latitude = 10
	longitude = 10
	sense = 20
	mmw_rate = 1
	legacy_rate = 1

	nNodes = int(sys.argv[1])
	nBeams = int(sys.argv[2])
	relief = int(sys.argv[5])
	seed = int(sys.argv[6])
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
        indexd = int(sys.argv[3])
        indexa = int(sys.argv[4])

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
	print erros[0]*1.0/erros[1]



	num = 0
	den = 0
        t_beamforming = ((time_arr['ssw']*nBeams)+(time_arr['sbifs']*(nBeams-1))+(2*time_arr['sifs'])+time_arr['sswfeedback']+time_arr['sswack'])
        # Time taken in OVERHEAD transmiting map and etc
        overhead = (nNodes*2*t_beamforming)+((nNodes-1)*time_arr['sifs'])+time_arr['txNum']+time_arr['sifs']+time_arr['txMap']
        schedule = scheduler.txSched(nodes,nNodes)
        #print schedule
        for i in schedule:
                overhead += time_arr['difs']+time_arr['txRts']+time_arr['sifs']+time_arr['txCts']+time_arr['sifs']
                #print i[0], nodes[i[0]].x, nodes[i[0]].y, '|', i[1], nodes[i[1]].x,nodes[i[1]].y, nodes[i[0]].angleList[i[1]][0]
                den += 1
                numberOfRetrials, time = scheduler.txCheck(nodes,proof,i[0],i[1], time_arr, relief)
                overhead += time
                #fair[i[0]]+=a
                num += numberOfRetrials

        #print "Average number of transmission retrials", round(1.0*num/den,6), "(due to angle missmatch)"
        #print "Number of transmissions scheduled", len(schedule)
        #print "Overhead caused by algorithm", overhead
        #overhead is not exactly the overhead, but the time taken to run all protocol stages
        mundimapp = overhead
        print mundimapp/1e6




	##################################################
	#
	#		CLUSTER PROTOCOL
	#
	##################################################
	nClusters = 4
	clusters = clusterFormation(nodes,nNodes,nClusters,leader)
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
				count = 0
				while clusters[count].count(j)==0: count+=1
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
	print erro*1.0/erros[1]
	
	maxCluster = len(clusters[0])
	for i in range(nClusters):
		test = len(clusters[i])
		if test > maxCluster: maxCluster = test

	maxCluster = int(nNodes/nClusters)
	overhead = t_beamforming*(maxCluster*2 + nClusters*2)
	overhead += time_arr['sifs']+ time_arr['txNum']+time_arr['sifs'] +time_arr['txMap']*nClusters
	
	for i in schedule:
		overhead += time_arr['difs']+time_arr['txRts']+time_arr['sifs']+time_arr['txCts']+time_arr['sifs']
                den += 1
                numberOfRetrials, time = scheduler.txCheck(nodes,proof,i[0],i[1], time_arr, relief)
                overhead += time
                num += numberOfRetrials
	print overhead/1e6
