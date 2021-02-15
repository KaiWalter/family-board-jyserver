#!/bin/bash

status_code=$(curl --write-out %{http_code} --silent --output /dev/null http://localhost:8080/health)

if [[ "$status_code" -eq 200 ]] ; then
  echo $(date -u --iso-8601=seconds) "OK"
else
  export DISPLAY=:0.0
  echo $(date -u --iso-8601=seconds) "Aborted $status_code->Refresh"
  xdotool key --window $(xdotool getactivewindow) ctrl+shift+r
fi