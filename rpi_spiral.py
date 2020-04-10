#!/usr/bin/python

import copy
import time

from sense_hat import SenseHat

# # # # # # # # # #

W = [255,255,255]
B = [0,0,0]
Cmap = [ [255,0,0], [255,255,0], [0,255,0], [0,255,255], [0,0,255], [255,0,255] ]
img = [
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W,
	W,W,W,W,W,W,W,W
]

sp = SenseHat()

for i in range(len(Cmap)):
	clr = Cmap[i]
	for r in range(1,8):
		for c in range(1,8):
			img[r*8+c] = clr
		sp.set_pixels( img )
		time.sleep( 0.2 )

sp.clear()
