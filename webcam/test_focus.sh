#!/bin/bash

#./init_cam.sh
# sudo ./usbreset /dev/bus/usb/001/010
#v4l2-ctl --set-ctrl=brightness=$bri
#v4l2-ctl --set-ctrl=contrast=$con
#v4l2-ctl --set-ctrl=white_balance_temperature=$wb
#v4l2-ctl --set-ctrl=white_balance_temperature_auto=1
#v4l2-ctl --set-ctrl=saturation=$sat
#v4l2-ctl --set-ctrl=gain=$gn
#v4l2-ctl --set-ctrl=sharpness=$shp

v4l2-ctl --set-ctrl=focus_auto=0

fswebcam -r 960x720 --title "bri=$bri con=$con sat=$sat wb=$wb gn=$gn shp=$shp" imagex_b${bri}_c${con}_s${sat}_w${wb}_g${gn}_sh${shp}.jpg

for fc in 0 17 34 51 68 102 136 170 204 238 255 
do
    v4l2-ctl --set-ctrl=focus_absolute=$fc
    fswebcam -r 960x720 --title "focus=$fc" image_fc${fc}.jpg
done


