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

cw_min = [8, 16, 32, 64]#,128, 256, 512]
nNodes = [1, 10, 20, 30, 40, 50]

for w in cw_min:
	plotter = []
	for n in nNodes:
		frac1 = 2.0/(w+1.0)
		frac2 = (w-1.0)/2.0
		expected_bo = frac2*slot
		pspt = frac1*(1.0 - frac1)**(n-1)
		pt = 1.0 - (1.0 - frac1)**n
		expected_tx = (n*pspt/pt)*(delta_tx+delta_difs+delta_ack+delta_sifs)
		expected_col = (1.0 - n*pspt/pt)*(delta_tx+delta_difs+delta_timeout)

		plotter.append(expected_bo+expected_tx+expected_col)
	plt.plot(nNodes,plotter)

 

plt.show()
