#!/usr/bin/python

import copy

# # # # # # # # # #

W = [255,255,255]
B = [0,0,0]
base_img = [
	W,W,W,W,B,B,B,B,
	W,W,W,W,B,B,B,B,
	W,W,B,B,B,B,B,B,
	W,W,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B,
	B,B,B,B,B,B,B,B
]

bit_pos = [
	[6,7,14,15],
	[22,23,30,31],
	[36,37,44,45], [38,39,46,47],
	[48,49,56,57], [50,51,58,59], [52,53,60,61]
]


# # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

def display_num( num ):
	img = copy.deepcopy( base_img )
	x = num
	for i in range(0,7):
		if( (x%2) == 1 ):
			plist = bit_pos[i]
			for j in plist:
				img[j] = W
		else:
			#img[pix] = B
			pass

		x = x // 2
		#print( "x=",x )

	#sp.set_pixels( img )
	i = 0
	txt = ''
	for r in range(8):
		for c in range(8):
			if( img[i] == W ):
				txt = txt + 'X'
			else:
				txt = txt + '.'
			i = i + 1
		txt = txt + '\n'
	print txt

# # # # # # # # # # # # # # # # # # # #
## # # # # # # # # # # # # # # # # # #
# # # # # # # # # # # # # # # # # # # #

while True:
	num = input( 'What number: ' )
	if( num >= 0 ):
		display_num( num )
	else:
		break
