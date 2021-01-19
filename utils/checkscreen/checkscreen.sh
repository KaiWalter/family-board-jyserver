#!/bin/bash

export DISPLAY=:0.0

raspi2png -p screen.png

python3 $(dirname "$0")/evalimage.py

if [ $? -eq 0 ]
then
    echo $(date -u --iso-8601=seconds) "OK"
else
    echo $(date -u --iso-8601=seconds) "Aborted->Refresh"
    xdotool key --window $(xdotool getactivewindow) ctrl+shift+r
fi
