import matplotlib.pyplot as plt
import math
import sys
r2 = math.sqrt(2)
pi = math.pi
halfpi = pi/2
r= 10.0
print r
num = 1000
passo = 0#r/num
print passo
di = 3  #[0]
alpha =[] #[0]
pe=[]
B = [pi/2, pi/4, pi/8, pi/16]
teste=[]
teste2=[]
count = 0
for b in B:
	#alpha.append(0)
	alpha = [0]
	x_axis = [0]
	passo = b/num
	pe.append(0)
	#alpha = b*float(sys.argv[1])
	A = (r**2)*b/2
	print 'Area total', A
	for i in range(1,num):
		#if count==0:
			#di.append(di[i-1]+passo)
		alpha.append(alpha[i-1]+passo)
		x_axis.append(alpha[i]/b)
		print alpha[i]
		if 1: #b <> halfpi:
			h = di*math.sin(alpha[i]) 
			y = (di*math.cos(alpha[i]) - h*math.tan(halfpi - b))
			a_par = y*h



			phi = math.asin(h/r)
			x1 = di*math.cos(alpha[i])
			x2 = di*(math.cos(alpha[i]) - (math.cos(b-alpha[i])*math.cos(b)))+math.sqrt(r**2 - (di**2)*(math.sin(b-alpha[i])**2))*math.cos(b)#(alpha)
			x3 = r*math.cos(phi)
			#print alpha[i], x2
			gama = math.acos(x2/r)

			a_tri1 = di*r*math.sin(gama-alpha[i])/2
			a_tri2 = r*di*math.sin(alpha[i]-phi)/2

			#a_ret = math.tan(b)*((x2-x1)**2)/2
			a_setora = (gama*r**2)/2#(x3/2)*math.sqrt((r**2)-(x3**2)) + ((x3**2)/2)*math.asin(x3/r)
			a_setorb = (phi*r**2)/2#(x2/2)*math.sqrt((r**2)-(x2**2)) + ((x2**2)/2)*math.asin(x2/r)
			a_base = (x3-x2)*h
			#pe.append(1 - ((a_par + a_set - a_tri)/A) )

			area = (di**2)*b/2
			pa= (a_par)/A#area
			pb= (a_setora - a_setorb - a_tri1 - a_tri2)/A#(a_ret + (a_setora - a_setorb - a_base))/A#(A - area) #(a_set-a_tri)/A

			#pe.append(pa*(area/A) + pb*(1-(area/A)))
			pe.append(1 - pa - pb + 2*pa*pb)
		else:
			h=di[i]*math.cos(alpha)
			y=di[i]*math.sin(alpha)
			phi = math.asin((r-di[i])*math.sin(b)/r)
			a_par = y*h
			a_set = phi*(r**2)/2
			a_tri = di[i]*math.cos(alpha)*(r-di[i])*math.sin(b)/2
			#a2 = (L-(di[i]*math.cos(alpha)))*(L-(di[i]*math.sin(alpha)))
			pa=a_par/A
			pb=(a_set-a_tri)/A
			pe.append(1 - (pa + pb))
		if i == num/2:
			print "Area Frontal", a_par, y, h
			print "Area oposta", a_setora - a_setorb - a_tri1 - a_tri2 
			print 'X1', x1, 'X2', x2, 'X3', x3
			#print a_par, a_ret, a_setora, a_setorb, a_base, a_setora - a_setorb
			print pa, pb, pe[i]
		if (round(pe[i+(count*num)],3)>0.498) and (round(pe[i+(count*num)],3)<0.501):
			teste.append(alpha[i])#di[i])
			teste2.append(pe[i+(count*num)])
	print len(alpha)
	count += 1
	if count == 1: plt.plot(x_axis,pe[(count-1)*num:count*num], label='B=4')
	elif count == 2: plt.plot(x_axis,pe[(count-1)*num:count*num], label='B=8')
	elif count == 3: plt.plot(x_axis,pe[(count-1)*num:count*num], label='B=16')
	elif count == 4: plt.plot(x_axis,pe[(count-1)*num:count*num], label='B=32')
	#plt.plot(teste,teste2,'o')

#plt.ylim(0,1)
plt.legend(loc=0)
plt.show()
#print alpha
