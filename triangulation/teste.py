import math

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

	def setBeams (self, nBeams):
		#set node's number o beams/sectors
		self.nBeams = nBeams
		#set node's beamwidth
		self.beamwidth = 2*pi/self.nBeams


def projections(r,node, adj):
	precision = 3
	Projection = []
	alpha = 2*pi/node.nBeams
        for n in range(node.nBeams):
                if (n*alpha - adj < pi) and (n*alpha-adj < pi) and ((n+1)*alpha-adj > pi):
                        x1 = node.x
                        x2 = node.x + r
                else:
                        x1 = node.x + r*math.cos(n*alpha - adj)
                        x2 = node.x + r*math.cos((n+1)*alpha - adj)
                        #x = max(x1,x2) 
		if x1< node.x and x2<node.x:
			if x1<x2: x2 = node.x
			else: x1 = node.x
		elif x1> node.x and x2>node.x:
			if x1<x2: x1 = node.x
			else: x2 = node.x 

                if (n*alpha-adj < pi) and (n*alpha-adj < (pi/2)) and ((n+1)*alpha-adj > (pi/2)):
                        y1 = node.y + r
                        y2 = node.y
                elif (n*alpha-adj > pi) and (n*alpha-adj < (3*pi/2)) and ((n+1)*alpha-adj > (3*pi/2)):
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


def intersections(i, j, ri, rj):	#(arrayI, arrayJ):
	theta1 = math.atan2(j.y-i.y,j.x-i.x)
	theta2 = math.atan2(i.y-j.y,i.x-j.x)
	if theta1 < 0: theta1 = 2*pi + theta1
	if theta2 < 0: theta2 = 2*pi + theta2

	print math.degrees(theta1), math.degrees(theta2)
	d = math.hypot(i.x-j.x, i.y-j.y)
	delta = 0.25*(math.sqrt((d+ri+rj)*(d+ri-rj)*(d-ri+rj)*(-d+ri+rj)))
	x1 = ((i.x+j.x)/2) + ((j.x-i.x)*((ri**2)-(rj**2))/(2*d**2)) + (2*(i.y-j.y)*delta/(d**2))
	x2 = ((i.x+j.x)/2) + ((j.x-i.x)*((ri**2)-(rj**2))/(2*d**2)) - (2*(i.y-j.y)*delta/(d**2))
	y1 = ((i.y+j.y)/2) + ((j.y-i.y)*((ri**2)-(rj**2))/(2*d**2)) - (2*(i.x-j.x)*delta/(d**2))
	y2 = ((i.y+j.y)/2) + ((j.y-i.y)*((ri**2)-(rj**2))/(2*d**2)) + (2*(i.x-j.x)*delta/(d**2))

	print x1,y1,x2,y2
	alpha=[0,0,0,0]
	alpha[0] = math.atan2(y1 - i.y,x1 - i.x)
	alpha[1] = math.atan2(- i.y + y2,-i.x + x2)

	alpha[2] = math.atan2(y1 - j.y,x1 - j.x)
	alpha[3] = math.atan2(y2 - j.y,x2 - j.x)
	
	#print math.degrees(alpha[0]), math.degrees(alpha[1]), math.degrees(alpha[2]), math.degrees(alpha[3])
	for m in range(len(alpha)):
		if alpha[m] < 0:
			alpha[m] = 2*pi + alpha[m]
		print math.degrees(alpha[m])
	distI = math.hypot(i.x-x2, i.y-y2)
	distJ = math.hypot(j.x-x2, j.y-y2)
	
	deltaI = math.atan2(i.y-y2,i.x-x2) - theta1
	deltaJ = math.atan2(j.y-y2,j.x-x2) - theta1
	print math.degrees(deltaI), math.degrees(deltaJ)
	
	newI = Node(distI*math.cos(deltaI), distI*math.sin(deltaI), 10)
	newJ = Node(distJ*math.cos(deltaJ), distJ*math.sin(deltaJ), 10)
	newI.setBeams(i.nBeams)
	newJ.setBeams(j.nBeams)
	
	print newI.x, newI.y, newJ.x, newJ.y

	projectionsI = projections(d, newI, theta1)
	projectionsJ = projections(d, newJ, theta1)
	print projectionsI
	print projectionsJ


if __name__ == "__main__":
	i = Node(0,0,10)#[0,0]
	j = Node(3,3,10)
	i.setBeams(3)
	j.setBeams(8)
	r = math.hypot(i.x-j.x, i.y-j.y)
        #Here starts an algorithm to detect an intersection betwen beams
        #The instersection of projections:
        #i is in quasi omni mode
        projectionsI = []
        projectionsJ = []

	projectionsI = projections(r, i,0)
	projectionsJ = projections(r, j,0)
	print projectionsI
	print projectionsJ
	print intersections(i,j,r,r)#(projectionsI, projectionsJ)

