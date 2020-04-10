#!/usr/bin/python

import copy

from sense_hat import SenseHat

# # # # # # # # # #

W = [255,255,255]
B = [0,0,0]
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

done = False

sp.set_pixels( img )

def joystick_push( event ):
	global done
	done = True

sp.stick.direction_any = joystick_push

# # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

while not done:
	pass

sp.clear()
