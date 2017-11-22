import sys
import math
import matplotlib.pyplot as plt

tx_rate = 24#e6
slot = 9
delta_tx = 1024*8.0/tx_rate
delta_sifs = 10
delta_difs = 28
delta_ack = 32.0*8.0/tx_rate
delta_timeout = 100

print delta_tx, delta_ack

cw_min = [8, 16, 32, 64] #,128] #, 256, 512]
nNodes = [10, 20, 30, 40, 50]

for w in cw_min:
	tx_time=[]
	plotter = []
	for n in nNodes:
		cumul = 0
		for s in range(1,8):
			prod = 1
			for k in range(1,s):
				if ((2**k)*w) <= 1024:
					tau_k = 2.0/((2**k)*w+1.0)

				pt = 1.0 - (1.0 - tau_k)**n
				ps = tau_k*(1.0 - tau_k)**(n-1)/pt

				expected_col = (1.0 - n*ps)
				prod = prod*expected_col

			tau_s = 2.0/((2**s)*w+1.0)
			pt = 1.0 - (1.0 - tau_s)**n
			ps = tau_s*(1.0 - tau_s)**(n-1)/pt
			expected_tx = (n*ps)#(delta_tx+delta_difs+delta_ack+delta_sifs)*k

			cumul += prod*expected_tx*s

		plotter.append(cumul)#expected_bo+expected_tx+expected_col)
		backoff = 0
		for a in range(int(cumul)):
			backoff += (((2**a)*w)-1.0)*slot/2

		time = delta_difs + backoff + (math.ceil(cumul)+1)*(delta_sifs+delta_ack+delta_tx)
		#time = time*(n-2)*(n-1)
		tx_time.append(time/1e6)

		for a in range(1,n):
			cumul = 0
			for s in range(1,8):
				prod = 1
				for k in range(1,s):
					if ((2**k)*w) <= 1024:
						tau_k = 2.0/((2**k)*w+1.0)

					pt = 1.0 - (1.0 - tau_k)**a
					ps = tau_k*(1.0 - tau_k)**(a-1)/pt

					expected_col = (1.0 - a*ps)
					prod = prod*expected_col

				tau_s = 2.0/((2**s)*w+1.0)
				pt = 1.0 - (1.0 - tau_s)**a
				ps = tau_s*(1.0 - tau_s)**(a-1)/pt
				expected_tx = (a*ps)

				cumul += prod*expected_tx*s

			backoff = 0
			for a in range(int(cumul)):
				backoff += (((2**a)*w)-1.0)*slot/2

			time += delta_difs + backoff + (math.ceil(cumul)+1)*(delta_sifs+delta_ack+delta_tx)
		#tx_time.append(time/1e6)

	plt.subplot(2,1,1)
	if w == 8: plt.plot(nNodes,plotter, 'b', label='CW$_{min}$=8')
	elif w == 16: plt.plot(nNodes,plotter, 'r', label='CW$_{min}$=16')
	elif w == 32: plt.plot(nNodes,plotter, 'g', label='CW$_{min}$=32')
	elif w == 64: plt.plot(nNodes,plotter, 'y', label='CW$_{min}$=64')
	elif w == 128: plt.plot(nNodes,plotter, 'k', label='CW$_{min}$=128')
	plt.ylabel("Expected transmissions")

	ax = plt.subplot(2,1,2)
	if w == 8: plt.plot(nNodes,tx_time, 'b', label='CW$_{min}$=8')
	elif w == 16: plt.plot(nNodes,tx_time, 'r', label='CW$_{min}$=16')
	elif w == 32: plt.plot(nNodes,tx_time, 'g', label='CW$_{min}$=32')
	elif w == 64: plt.plot(nNodes,tx_time, 'y', label='CW$_{min}$=64')
	elif w == 128: plt.plot(nNodes,tx_time, 'k', label='CW$_{min}$=128')
	plt.ylabel("Expected time ($S$)")
 	plt.xlabel("Number of Nodes")
	

#for i in xrange(5):
#    line, = ax.plot(x, i * x, label='$y = %ix$'%i)

# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.9])

plt.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, -0.20))
plt.show()
