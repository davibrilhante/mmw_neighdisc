import math
import random

pi=math.pi




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
                #       return [0, round(maptable[i][1],2), 'l']
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





def mapCheck(nodes, nNodes, leader, relief, proof):
	num = 0
	den = 0

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
			if j == leader: 
				temp.append(beamforming(nodes,chosen,i))
			else:
				nodes[chosen].angleList.append(estimating(nodes,chosen, i, leader, nodes[leader].angleList))
				temp.append(beamforming(nodes,chosen,i))
		proof.append(temp)

		template = "{0:15}"	
		for i in range(nNodes):
			den = den + 1
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
	return [num, den, averageBeamError]
