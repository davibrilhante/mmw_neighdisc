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

cw_min = [16, 32, 64]#,128, 256, 512]
nNodes = [10, 20, 30, 40, 50]

for w in cw_min:
	plotter = []
	time = 0
	tau=2.0/(w+1)
	for n in nNodes:
		pt = 1.0 - (1.0 - tau)**n
		ps = n*tau*((1-tau)**(n-1))/pt

		expected_bo = (1-pt)*slot

		expected_tx = (ps*pt)*(delta_tx+delta_difs+delta_ack+delta_sifs)
		expected_col = (1.0 - ps)*pt*(delta_tx+delta_difs+delta_timeout)

		#plotter.append(5*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6))
		time = (n*(n-2))*5.0*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6)
		for k in range(1,n):
			pt = 1.0 - (1.0 - tau)**k
			ps = k*tau*((1-tau)**(k-1))/pt

			expected_bo = (1-pt)*slot

			expected_tx = (ps*pt)*(delta_tx+delta_difs+delta_ack+delta_sifs)
			expected_col = (1.0 - ps)*pt*(delta_tx+delta_difs+delta_timeout)

			time += 5*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6)
			#plotter.append(5*(expected_bo+expected_tx+expected_col)/(ps*pt*1e6))
		plotter.append(time)
	#plt.plot(nNodes,plotter)
	ax = plt.subplot(1,1,1)
	if w == 8: plt.plot(nNodes,plotter, 'b', label='CW$_{min}$=8')
        elif w == 16: plt.plot(nNodes,plotter, 'r', label='CW$_{min}$=16')
        elif w == 32: plt.plot(nNodes,plotter, 'g', label='CW$_{min}$=32')
        elif w == 64: plt.plot(nNodes,plotter, 'y', label='CW$_{min}$=64')
        elif w == 128: plt.plot(nNodes,plotter, 'k', label='CW$_{min}$=128')
        plt.ylabel("Expected transmissions $(s)$")

 
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.2,
                 box.width, box.height * 0.9])
plt.xlabel("Number of Nodes")
plt.legend(loc='upper center', ncol=4, bbox_to_anchor=(0.5, -0.20))
plt.show()
