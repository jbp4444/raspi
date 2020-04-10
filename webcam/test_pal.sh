#!/bin/bash


bri=0
cont=28
sat=64
hue=0
gain=0
sharp=3

# available sizes:
# 352x288, 640x480, 800x600, 960x720, 1280x720

# should not be needed, but just in case ... reset the camera
# sudo ./usbreset /dev/bus/usb/001/010

# basic controls
# : v4l2-ctl --list-ctrls
# : v4l2-ctl --list-ctrls-menus
# : alternately, use fswebcam --list-controls (and --set key=val)
v4l2-ctl --set-ctrl=brightness=$bri
v4l2-ctl --set-ctrl=contrast=$cont
v4l2-ctl --set-ctrl=saturation=$sat
v4l2-ctl --set-ctrl=hue=$hue
v4l2-ctl --set-ctrl=gain=$gain
v4l2-ctl --set-ctrl=sharpness=$sharp

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

# capture the pic
# : skip a few frames to let camera calc any "auto" settings
fswebcam --no-banner --skip 2 -r 640x480 pic_$dt.jpg


v4l2-ctl --set-ctrl=sharpness=$shp


for pal in PNG JPEG MJPEG RGB32 RGB24 BGR32 BGR24 YUYV UYVY YUV420P BAYER SGBRG8 SGRBG8 RGB565 RGB555 GREY
do
    fswebcam -r 960x720 --skip 2 -p $pal --title "pal=$pal bri=$bri con=$con sat=$sat wb=$wb gn=$gn shp=$shp" image_${pal}.jpg
done


