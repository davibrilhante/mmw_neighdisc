import math
import random



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






