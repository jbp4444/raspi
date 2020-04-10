#!/bin/bash

# available sizes:
# 352x288, 640x480, 800x600, 960x720, 1280x720

# should not be needed, but just in case ... reset the camera
# sudo ./usbreset /dev/bus/usb/001/010

# basic controls
# : v4l2-ctl --list-ctrls
# : v4l2-ctl --list-ctrls-menus
# : alternately, use fswebcam --list-controls (and --set key=val)
v4l2-ctl --set-ctrl=brightness=128
v4l2-ctl --set-ctrl=contrast=32
v4l2-ctl --set-ctrl=saturation=32
v4l2-ctl --set-ctrl=gain=64
v4l2-ctl --set-ctrl=sharpness=22

# white balance
v4l2-ctl --set-ctrl=white_balance_temperature_auto=1
# : manual: set auto=0 and then set temp
#v4l2-ctl --set-ctrl=white_balance_temperature_auto=0
#v4l2-ctl --set-ctrl=white_balance_temperature=2800

# exposure
# : 1=Manual Mode; 3=Aperture priority mode
v4l2-ctl --set-ctrl=exposure_auto=0
#v4l2-ctl --set-ctrl=exposure_auto=1
#v4l2-ctl --set-ctrl=exposure_absolute=166

# date-stamp each file
dt=$(date +%Y%m%d%H%M%S)

# capture the pic
fswebcam --no-banner -r 640x480 pic_$dt.jpg

