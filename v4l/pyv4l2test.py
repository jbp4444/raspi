#!/usr/bin/python
#
# https://github.com/duanhongyi/pyv4l2

from pyv4l2.frame import Frame
from pyv4l2.control import Control
from PIL import Image

control = Control("/dev/video0")
control.get_controls()
# control.get_control_value(9963776)
# control.set_control_value(9963776, 8)

frame = Frame('/dev/video0')
image_data = frame.get_frame()

image = Image.frombytes("RGB", (size_x, size_y), image_data)
image.save("image.jpg")
print "Saved image.jpg (Size: " + str(size_x) + " x " + str(size_y) + ")"

