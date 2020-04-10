#!/usr/bin/python

import socket
import fcntl
import struct
import time
from sense_hat import SenseHat

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		return socket.inet_ntoa(fcntl.ioctl(
			s.fileno(),
			0x8915,  # SIOCGIFADDR
			struct.pack('256s', ifname[:15])
		)[20:24])
	except:
		return 'ERROR'

time.sleep( 5 )

sense = SenseHat()

#print get_ip_address('eth0')
#print get_ip_address('wlan0')

msg = ''
x = get_ip_address('eth0')
if( x != 'ERROR'):
	msg = msg + ' eth0=' + x
x = get_ip_address('wlan0')
if( x != 'ERROR'):
	msg = msg + ' wlan0=' + x

for i in range(1,10):
	sense.show_message( msg )
