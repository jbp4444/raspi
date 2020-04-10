#!/bin/bash

# available sizes:
# 352x288, 640x480, 800x600, 960x720, 1280x720

# should not be needed, but just in case ... reset the camera
# sudo ./usbreset /dev/bus/usb/001/010

# basic controls
# : v4l2-ctl --list-ctrls
# : v4l2-ctl --list-ctrls-menus
# : alternately, use fswebcam --list-controls (and --set key=val)
v4l2-ctl --set-ctrl=brightness=0
v4l2-ctl --set-ctrl=contrast=28
v4l2-ctl --set-ctrl=saturation=64
v4l2-ctl --set-ctrl=hue=0
v4l2-ctl --set-ctrl=gain=0
v4l2-ctl --set-ctrl=sharpness=3

# white balance
v4l2-ctl --set-ctrl=white_balance_temperature_auto=1
# : manual: set auto=0 and then set temp
#v4l2-ctl --set-ctrl=white_balance_temperature_auto=0
#v4l2-ctl --set-ctrl=white_balance_temperature=2800

# exposure
# : 1=Manual Mode; 3=Aperture priority mode
v4l2-ctl --set-ctrl=exposure_auto=3
#v4l2-ctl --set-ctrl=exposure_auto=1
#v4l2-ctl --set-ctrl=exposure_absolute=166

# date-stamp each file
dt=$(date +%Y%m%d%H%M%S)

# capture the pic
# : skip a few frames to let camera calc any "auto" settings
#fswebcam --no-banner --skip 2 -r 640x480 pic_$dt.jpg
v4l2-ctl --set-ctrl=backlight_compensation=0
fswebcam --no-banner --skip 2 --rotate 270 -r 480x640 pic_0_$dt.jpg
v4l2-ctl --set-ctrl=backlight_compensation=1
fswebcam --no-banner --skip 2 --rotate 270 -r 480x640 pic_1_$dt.jpg
v4l2-ctl --set-ctrl=backlight_compensation=2
fswebcam --no-banner --skip 2 --rotate 270 -r 480x640 pic_2_$dt.jpg

