import matplotlib.pyplot as plt
import math
import sys
r2 = math.sqrt(2)
pi = math.pi
halfpi = pi/2
r= 10.0
print r
num = 1000
passo = r/num
print passo
di = [0]
pe=[]
B = [pi/2, pi/4, pi/8, pi/16]
teste=[]
teste2=[]
count = 0
for b in B:
	pe.append(0)
	alpha = b*float(sys.argv[1])
	A = (r**2)*b/2
	print 'Area total', A
	for i in range(1,num):
		if count==0:
			di.append(di[i-1]+passo)
		if 1: #b <> halfpi:
			h = di[i]*math.sin(alpha) 
			y = (di[i]*math.cos(alpha) - h*math.tan(halfpi - b))
			a_par = y*h



			phi = math.asin(h/r)
			x1 = di[i]*math.cos(alpha)
			x2 = di[i]*(math.cos(alpha) - (math.cos(b-alpha)*math.cos(b)))+math.sqrt(r**2 - (di[i]**2)*(math.sin(b-alpha)**2))*math.cos(b)#(alpha)
			x3 = r*math.cos(phi)
			gama = math.acos(x2/r)

			a_tri1 = di[i]*r*math.sin(gama-alpha)/2
			a_tri2 = r*di[i]*math.sin(alpha-phi)/2

			#a_ret = math.tan(b)*((x2-x1)**2)/2
			a_setora = (gama*r**2)/2#(x3/2)*math.sqrt((r**2)-(x3**2)) + ((x3**2)/2)*math.asin(x3/r)
			a_setorb = (phi*r**2)/2#(x2/2)*math.sqrt((r**2)-(x2**2)) + ((x2**2)/2)*math.asin(x2/r)
			a_base = (x3-x2)*h
			#pe.append(1 - ((a_par + a_set - a_tri)/A) )

			area = (di[i]**2)*b/2
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
		if i == 500:
			print "Area Frontal", a_par
			#print "Area oposta", a_ret + (a_setora - a_setorb - a_base) 
			print 'X1', x1, 'X2', x2, 'X3', x3
			#print a_par, a_ret, a_setora, a_setorb, a_base, a_setora - a_setorb
			print pa, pb, pe[i]
		if (round(pe[i+(count*1000)],3)>0.498) and (round(pe[i+(count*1000)],3)<0.501):
			teste.append(di[i])
			teste2.append(pe[i+(count*1000)])
	count += 1
	if count == 1: plt.plot(di,pe[(count-1)*1000:count*1000], label='B=4')
	elif count == 2: plt.plot(di,pe[(count-1)*1000:count*1000], label='B=8')
	elif count == 3: plt.plot(di,pe[(count-1)*1000:count*1000], label='B=16')
	elif count == 4: plt.plot(di,pe[(count-1)*1000:count*1000], label='B=32')
	plt.plot(teste,teste2,'o')

plt.ylim(0,1)
plt.legend(loc=0)
plt.show()
