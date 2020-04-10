#!/usr/bin/python

from sense_hat import SenseHat

s = SenseHat()

X = [255,0,0]
O = [0,255,255]

data = [
O,O,O,X,X,X,O,O,
O,O,O,X,X,X,O,O,
O,O,O,X,X,X,O,O,
O,O,O,X,X,X,O,O,
X,X,X,O,O,O,X,X,
X,X,X,O,O,O,X,X,
X,X,X,O,O,O,X,X,
X,X,X,O,O,O,X,X
]

s.set_pixels(data)

