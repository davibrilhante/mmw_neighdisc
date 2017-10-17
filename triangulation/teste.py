import math

pi = math.pi

def projections(nbeams,r,node):
	precision = 3
	Projection = []
	alpha = 2*pi/nbeams
        for n in range(nbeams):
                if (n*alpha < pi) and (n*alpha < pi) and ((n+1)*alpha > pi):
                        x1 = node[0]
                        x2 = node[0] + r
                else:
                        x1 = node[0] + r*math.cos(n*alpha)
                        x2 = node[0] + r*math.cos((n+1)*alpha)
                        #x = max(x1,x2) 
		if x1< node[0] and x2<node[0]:
			if x1<x2: x2 = node[0]
			else: x1 = node[0]
		elif x1> node[0] and x2>node[0]:
			if x1<x2: x1 = node[0]
			else: x2 = node[0] 

                if (n*alpha < pi) and (n*alpha < (pi/2)) and ((n+1)*alpha > (pi/2)):
                        y1 = node[1] + r
                        y2 = node[1]
                elif (n*alpha > pi) and (n*alpha < (3*pi/2)) and ((n+1)*alpha > (3*pi/2)):
                        y1 = node[1]
                        y2 = node[1] - r
                else:
                        y1 = node[1] + r*math.sin(n*alpha)
                        y2 = node[1] + r*math.sin((n+1)*alpha)
		
		if y1< node[1] and y2<node[1]:
                        if y1<y2: y2 = node[1]
                        else: y1 = node[1]
                elif y1> node[1] and y2>node[1]:
                        if y1<y2: y1 = node[1]
                        else: y2 = node[1]

                Projection.append([[round(x1,precision),round(x2,precision)],
				   [round(y1,precision),round(y2,precision)]])
                #print "[",x1,",",x2,"] [",y1,",",y2,"]"
        return Projection


def intersections(arrayI, arrayJ):
	array = []
	countI = 0
	for i in arrayI:
		countJ = 0
		for j in arrayJ:
			#x comparison
			print
			print "(",i[0][0],",",i[0][1],") , (",i[1][0],",",i[1][1],")"
			print "(",j[0][0],",",j[0][1],") , (",j[1][0],",",j[1][1],")"
			print
			if i[0][0]<=j[0][0] or i[0][1]>=j[0][1]:
				#y comparison
				if i[1][0]<=j[1][0] or i[1][1]>=j[1][1]:
					#ok, there's an intersection
					intersectionX = [min(i[0][0],j[0][0]),max(i[0][1],j[0][1])]
					intersectionY = [min(i[1][0],j[1][0]),max(i[1][1],j[1][1])]
					array.append([countI, countJ, intersectionX, intersectionY])
			countJ += 1
		countI += 1			
	return array



if __name__ == "__main__":
	i = [0,0]
	j = [3,3]
	nbeamsI = 3
	nbeamsJ = 8
	r = math.hypot(i[0]-j[0], i[1]-j[1])
        #Here starts an algorithm to detect an intersection betwen beams
        #The instersection of projections:
        #i is in quasi omni mode
        projectionsI = []
        projectionsJ = []
        alpha = 2*pi/nbeamsI
        '''for n in range(nbeamsI):
		if (n*alpha < pi) and (n*alpha < pi) and ((n+1)*alpha > pi):
			x1 = i[0]
                        x2 = i[0] + r
                else:
                        x1 = i[0] + r*math.cos(n*alpha)
                        x2 = i[0] + r*math.cos((n+1)*alpha)
			#x = max(x1,x2)	

                if (n*alpha < pi) and (n*alpha < (pi/2)) and ((n+1)*alpha > (pi/2)):
			y1 = i[1] + r
			y2 = i[1]
                elif (n*alpha > pi) and (n*alpha < (3*pi/2)) and ((n+1)*alpha > (3*pi/2)):
			y1 = i[1]
			y2 = i[1] - r
                else:
                        y1 = i[1] + r*math.sin(n*alpha)
                        y2 = i[1] + r*math.sin((n+1)*alpha)
		projectionsI.append([[x1,x2],[y1,y2]])
		#print "[",x1,",",x2,"] [",y1,",",y2,"]"
	print projectionsI'''
        #j is in normal mode
        '''for n in range(nbeamsJ):
		if (n*alpha < pi) and (n*alpha < pi) and ((n+1)*alpha > pi):
			x1 = j[0]
                        x2 = j[0] + r
                else:
                        x1 = j[0] + r*math.cos(n*alpha)
                        x2 = j[0] + r*math.cos((n+1)*alpha)
			#x = max(x1,x2)	

                if (n*alpha < pi) and (n*alpha < (pi/2)) and ((n+1)*alpha > (pi/2)):
			y1 = j[1] + r
			y2 = j[1]
                elif (n*alpha > pi) and (n*alpha < (3*pi/2)) and ((n+1)*alpha > (3*pi/2)):
			y1 = j[1]
			y2 = j[1] - r
                else:
                        y1 = j[1] + r*math.sin(n*alpha)
                        y2 = j[1] + r*math.sin((n+1)*alpha)
		projectionsJ.append([[x1,x2],[y1,y2]])
	print projectionsJ'''

	projectionsI = projections(nbeamsI, r, i)
	projectionsJ = projections(nbeamsJ, r, j)
	print projectionsI
	print projectionsJ
	print intersections(projectionsI, projectionsJ)

