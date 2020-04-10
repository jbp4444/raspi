#!/usr/bin/python

import time
from PIL import Image
import select
import v4l2capture

# Open the video device.
video = v4l2capture.Video_device("/dev/video0")

# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
#size_x, size_y = video.set_format(1280, 1024)
size_x, size_y = video.set_format(640,480)

# Create a buffer to store image data in. This must be done before
# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
# raises IOError.
video.create_buffers(1)

# Send the buffer to the device. Some devices require this to be done
# before calling 'start'.
video.queue_all_buffers()

# Start the device. This lights the LED if it's a camera that has one.
video.start()

t1 = time.time()

for ctr in range(100):
	# Wait for the device to fill the buffer.
	select.select((video,), (), ())

	# The rest is easy :-)
	#image_data = video.read()
	image_data = video.read_and_queue()

	image = Image.frombytes("RGB", (size_x, size_y), image_data)
	image.save("image"+str(ctr)+".jpg")
	#print "Saved image"+str(ctr)+".jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"

	time.sleep( 0.1 )
	ctr = ctr + 1

t2 = time.time()

video.close()

print( '100 iterations took %.2f sec' % (t2-t1) )

