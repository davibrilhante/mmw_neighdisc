import matplotlib.pyplot as plt
import numpy
import random
import math
import sys

pi = math.pi
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

### EIXO Y: PROBABILIDADE DE ERRO (0,1)
### EIXO X: BEAMWIDTH (10,120)

di = 3.0
dj = 5.0
#il = math.radians(60)
#jl = math.radians(120)

alpha = math.radians(int(sys.argv[1]))
erro = float(sys.argv[2])

li = (3*pi/2)-(alpha/2.0)
lj = (3*pi/2)+(alpha/2.0)
'''xi = di*math.cos((3*pi/2)-(alpha/2.0))
yi = di*math.sin((3*pi/2)-(alpha/2.0))
xj = dj*math.cos((3*pi/2)+(alpha/2.0))
yj = dj*math.sin((3*pi/2)+(alpha/2.0))'''
if li > pi:
	il = li - pi
else:
	il = li + pi

C1 = math.sin(alpha)
C3 = math.cos(alpha)
C2 = 1.0/math.tan(alpha)#numpy.divide(C3,C1)#1.0/math.tan(alpha)

### NAO SEI SE ISSO VAI FUNCIONAR
theta = round(il - math.atan2((dj*C1),(di - dj*C3)), 2)
#theta = math.atan2((dj*C1),(di - dj*C3))
if theta < 0:
	theta = 2*pi + theta

print bcolors.BOLD,"theta =",math.degrees(theta),bcolors.ENDC
### TERMINEI A GAMBIARRA AQUI
angles = []
angles.append((di - erro*di)/((dj + erro*dj)*C1) - C2) 	###A
angles.append((di/(dj*C1)) - C2)			###B
angles.append((di + erro*di)/((dj - erro*dj)*C1) - C2)	###C
angles.sort()
A = angles[0]
B = angles[1]
C = angles[2]
print angles
print A, B, C ###min(angles), max(angles)
print math.degrees(math.atan2(1.0,A)), math.degrees(math.atan2(1.0,B)), math.degrees(math.atan2(1.0,C))


'''print "\n###########################################\n            MEU OBJETIVO\n\t  ",
if il < math.atan2(1.0,A):
	print 360 + round(math.degrees(il - math.atan2(1.0,A)),2),
else:
	print round(math.degrees(il - math.atan2(1.0,A)),2), 
if il < math.atan2(1.0,B):
	print 360 + round(math.degrees(il - math.atan2(1.0,B)),2),
else:
	print round(math.degrees(il - math.atan2(1.0,B)),2), 
if il < math.atan2(1.0,C):
	print 360 + round(math.degrees(il - math.atan2(1.0,C)),2)
else:
	print round(math.degrees(il - math.atan2(1.0,C)),2)
print "###########################################"

if il < math.atan2(1.0,C):
	A = (1 + math.tan(2*pi + il)/A)/(math.tan(2*pi + il) - 1.0/A)
	B = (1 + math.tan(2*pi + il)/B)/(math.tan(2*pi + il) - 1.0/B)
	C = (1 + math.tan(2*pi + il)/C)/(math.tan(2*pi + il) - 1.0/C)
else:
	A = (1 + math.tan(il)/A)/(math.tan(il) - 1.0/A)
	B = (1 + math.tan(il)/B)/(math.tan(il) - 1.0/B)
	C = (1 + math.tan(il)/C)/(math.tan(il) - 1.0/C)
	
#A = round(1/numpy.tan(math.atan2(1.0,A) - il),2)
#B = round(1/numpy.tan(math.atan2(1.0,B) - il),2)
#C = round(1/numpy.tan(math.atan2(1.0,C) - il),2)'''



D = (di*C1)/(2.0*dj)
E = (di - erro*di)/C1
F = (di + erro*di)/C1
G = (dj + erro*dj)
H = (dj - erro*dj)
#print A, B, C
#print math.degrees(math.atan2(1.0,A)), math.degrees(math.atan2(1.0,B)), math.degrees(math.atan2(1.0,C))
#print C2

K = D*((G**2)*(B - A) - (E**2)*(1/(A+C2) - (1/(B+C2))))
L = D*( - (H**2)*(C - B) + (F**2)*(1/(B+C2) - (1/(C+C2))))
print K, L

#beamwidth = numpy.arange(15,95,5)
beamwidth = [12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120]
plot = []



for i in beamwidth:
	beamTheta = int(math.degrees(theta)/i)
	if beamTheta > int(360/i): beamTheta = beamTheta - int(360/i)
	elif beamTheta < 0:  beamTheta = beamTheta + int(360/i)	
	###print math.ceil(math.degrees(il)/i)
	###print beamTheta*i, beamTheta*i + i

	if beamTheta < math.ceil(math.degrees(il)/i):
		beta2 = math.degrees(il) - beamTheta*i
	else:
		beta2 = math.degrees(il) - (beamTheta*i - 360)

	#beta1 = beamTheta*i
	beta1 = beta2-i #(beamTheta+1)*i
	x = numpy.divide(math.cos(math.radians(beta1)), math.sin(math.radians(beta1))) ###cotangente(beta1)
	if type(x) <> type(1.0): x = round(x,2)
        y = numpy.divide(math.cos(math.radians(beta2)), math.sin(math.radians(beta2))) ###cotangente(beta2)
	print "\n",beamTheta, beta1,"(",x,")", beta2,"(",y,")"
	if type(y) <> type(1.0): y = round(y,2)
	
	if y < A:
		### CASO 1 - ERROU O SETOR (1 SETOR A MENOS)
		if x < A:
			print "CASO 1"
			plot.append(1)

		###CASO 2
		elif ( x >= A and x < B):
			print "CASO 2"
			part1 = (G**2)*(x - A)
			part2 = (E**2)*(1/(A+C2) - 1/(x+C2))
			print 1 - D*(part1 - part2)
			plot.append(1 - D*(part1 - part2))

		###CASO 3
		#elif ( x >= B and x <= C) and (y >= B and y <= C):
		elif (x>=B and x <C):
			print "CASO 3"
			part1 = (F**2)*(1/(B+C2) - 1/(x+C2))
			part2 = (H**2)*(x - B)
			print K, D, B, C2, x, part1, part2
			print 1 - K - D*(part1 - part2)
			plot.append(1 - D*(part1 - part2))#'''

		###CASO 4
		#elif (x >= B and x <= C) and (y >= A and y < B):
		elif (x >= C):
			print "CASO 4"
			print 1 - K - L
			plot.append(1 - K - L)

	###CASO 5
	elif (y >= A and y < B):
	#elif (x >= A and x < B) and (y >= A and y < B):
		if (x >= A and x < B):
			print "CASO 5"
			part1 = (G**2)*(x-y)
                	part2 = (E**2)*(1/(y+C2) - 1/(x+C2))
                	print 1 - D*(part1 - part2)

		###CASO 6
		#elif (y  < A) and ( x >= A and x < B):
		elif (x >= B and x < C):
			print "CASO 6"
			part1 = (F**2)*(1/(B+C2) - 1/(x+C2))
			part2 = (H**2)*(x - B)
			print 1 - K - D*(part1 - part2)
			part3 = (G**2)*(y-A)
			part4 = (E**2)*(1/(A+C2) - 1/(y+C2))
			print D*(part3-part4)	
			plot.append(1 - D*(part1 - part2) + D*(part3-part4))
	
		###CASO 7
		#elif (y>=A and y < B) and (x > C):
		elif (x >= C):
			print "CASO 7"	
			part1 = (G**2)*(y-A)
			part2 = (E**2)*(1/(A+C2) - 1/(y+C2))
			print 1 - K + D*(part1 - part2)
			plot.append (1 + D*(part1 - part2))
	###CASO 8
	#elif (y < A) and (x > C):
	if (y >= B and y < C):
		if  (x >= B and x < C):
			print "CASO 8"
			plot.append(0)
		### CASO 9
		elif (x >= C):
			print "CASO 9"

	###CASO 10 - ERROU O SETOR (UM SETOR A MAIS)
	elif (y >= C) and (x >= C):
		print "CASO 10"
		plot.append(1)
		'''part1 = (F**2)*(1/(B+C2)- 1/(x+C2)) 
                part2 = (H**2)*(x-B)
                sum1 = D*(part1 - part2)

		print 1 - sum1
		plot.append(1-sum1)'''



plt.plot(beamwidth, plot)
#plt.plot(plot)
plt.show()