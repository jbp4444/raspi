#!/bin/bash

bri=0
con=28
sat=64
wb=auto
gn=0
shp=3

#./init_cam.sh
# sudo ./usbreset /dev/bus/usb/001/010
v4l2-ctl --set-ctrl=brightness=$bri
v4l2-ctl --set-ctrl=contrast=$con
#v4l2-ctl --set-ctrl=white_balance_temperature=$wb
v4l2-ctl --set-ctrl=white_balance_temperature_auto=1
v4l2-ctl --set-ctrl=saturation=$sat
v4l2-ctl --set-ctrl=gain=$gn
v4l2-ctl --set-ctrl=sharpness=$shp

fswebcam -r 960x720 --title "bri=$bri con=$con sat=$sat wb=$wb gn=$gn shp=$shp" imagex_b${bri}_c${con}_s${sat}_w${wb}_g${gn}_sh${shp}.jpg

#for bri in -64 -32 -16 0 16 32 64
for gn in 0 10 20 30 40 50 60 70 80 90 100
do
    v4l2-ctl --set-ctrl=gain=$gn
    fswebcam -r 960x720 --title "bri=$bri con=$con sat=$sat wb=$wb gn=$gn shp=$shp" image_b${bri}_c${con}_s${sat}_w${wb}_g${gn}_sh${shp}.jpg
done


