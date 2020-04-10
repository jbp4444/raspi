#!/usr/bin/python

import copy

from sense_hat import SenseHat

# # # # # # # # # #

W = [255,255,255]
B = [0,0,0]
base_img = [
	W,W,W,B,B,B,B,B,
	W,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B
]

bit_pos = [
	4,5,6,
	12,13,14,15,
	18,19,20,21,22,23,
	24,25,26,27,28,29,30,31,
	32,33,34,35,36,37,38,39,
	40,41,42,43,44,45,46,47,
	48,49,50,51,52,53,54,55,
	57,58,59,60,61,62
]

sp = SenseHat()

# # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

def display_num( num ):
	img = copy.deepcopy( base_img )
	x = num
	for i in range(0,50):
		pix = bit_pos[i]
		if( (x%2) == 1 ):
			img[pix] = W
		else:
			#img[pix] = B
			pass

		x = x // 2
		print( "x=",x )

	sp.set_pixels( img )

def joystick_push( event ):
	sp.clear()
sp.stick.direction_any = joystick_push

# # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

while True:
	num = input( 'What number: ' )
	if( num > 0 ):
		display_num( num )
	else:
		break

sp.clear()
