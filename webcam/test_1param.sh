#!/bin/bash

bri=128
con=32
sat=32
wb=auto
gn=64
shp=22

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

for shp in 32 64 80 96 128 255
do
    v4l2-ctl --set-ctrl=sharpness=$shp
    fswebcam -r 960x720 --title "bri=$bri con=$con sat=$sat wb=$wb gn=$gn shp=$shp" image_b${bri}_c${con}_s${sat}_w${wb}_g${gn}_sh${shp}.jpg
done


