#!/usr/bin/python

import os
import v4l2capture

file_names = [x for x in os.listdir("/dev") if x.startswith("video")]
file_names.sort()

for file_name in file_names:
	path = "/dev/" + file_name
	print path
	try:
		video = v4l2capture.Video_device(path)
		driver, card, bus_info, capabilities = video.get_info()
		print "    driver:       %s\n    card:         %s" \
			"\n    bus info:     %s\n    capabilities: %s" % (
				driver, card, bus_info, ", ".join(capabilities))
		video.close()
	except IOError, e:
		print "    " + str(e)

print( 'v4l2capture functions:' )
video = v4l2capture.Video_device( '/dev/video0' )
lst = dir( video )
for l in lst:
	if( l[:2] != '__' ):
		print( '   %s'%(l) )	

