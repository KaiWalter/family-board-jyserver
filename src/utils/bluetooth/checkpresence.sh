#!/bin/bash

export DISPLAY=:0.0

dp=$(vcgencmd display_power)

presence=$(python3 $(dirname "$0")/scan_bt.py)

echo $(date -u --iso-8601=seconds) presence: $presence display: $dp

if [[ $presence -eq "True" ]]
then
    if [[ "$dp" == "display_power=0" ]]; then vcgencmd display_power 1; fi
else
    if [[ "$dp" == "display_power=1" ]]; then vcgencmd display_power 0; fi
fi