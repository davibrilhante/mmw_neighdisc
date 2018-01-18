import math
import random

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





def createNet(latitude, longitude, sense, nNodes, nBeams,leader):
	nodes = []
        lista = []
        nodes.append(Node(0,0,sense))
        nodes[leader].Id = 0
        nodes[leader].setBeams(nBeams)
        lista.append([nodes[leader].x, nodes[leader].y])
        for i in range(1,nNodes):
                nodes.append(Node(random.randint(-(latitude/2),latitude/2),random.randint(-(longitude/2),longitude/2),sense))
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

	return nodes
