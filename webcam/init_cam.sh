#!/bin/bash

# basic controls
v4l2-ctl --set-ctrl=brightness=128
v4l2-ctl --set-ctrl=contrast=32
v4l2-ctl --set-ctrl=saturation=32
v4l2-ctl --set-ctrl=gain=64
v4l2-ctl --set-ctrl=sharpness=22

# manual white balance
v4l2-ctl --set-ctrl=white_balance_temperature_auto=1
#v4l2-ctl --set-ctrl=white_balance_temperature_auto=0
#v4l2-ctl --set-ctrl=white_balance_temperature=2800

# manual exposure
# : 1=Manual Mode; 3=Aperture priority mode
v4l2-ctl --set-ctrl=exposure_auto=1
#v4l2-ctl --set-ctrl=exposure_auto=0
#v4l2-ctl --set-ctrl=exposure_absolute=166

