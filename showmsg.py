#!/usr/bin/python

import sys
from sense_hat import SenseHat

sense = SenseHat()

msg = "Hello World!"
if( len(sys.argv) > 1 ):
	msg = sys.argv[1]

sense.show_message( msg )
