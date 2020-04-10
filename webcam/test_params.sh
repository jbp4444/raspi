#!/bin/bash

#./init_cam.sh

#for bri in 32 64 96 128 255
for bri in 128 160
do
  for con in 32 64 96
  do
    #for sat in 32 64 96 128 255
    for sat in 32 64
    do
      #for wb in 2800 3300 3800 4300 4800 5300 5800 6300 6500
      for wb in 3800 4800 5800
      do
        for gn in 64 80
        do
		# sudo ./usbreset /dev/bus/usb/001/010
		v4l2-ctl --set-ctrl=brightness=$bri
		v4l2-ctl --set-ctrl=contrast=$con
		v4l2-ctl --set-ctrl=white_balance_temperature=$wb
		v4l2-ctl --set-ctrl=saturation=$sat
		v4l2-ctl --set-ctrl=gain=$gn
		fswebcam -r 960x720 --title "bri=$bri con=$con sat=$sat wb=$wb gn=$gn" image_b${bri}_c${con}_s${sat}_w${wb}_g${gn}.jpg

		sleep 3
        done
      done
    done
  done
done


