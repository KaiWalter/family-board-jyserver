# scan Bluetooth for devices in range and report to board

import bluetooth
import time
import requests
import json

headers = {'Content-Type': 'application/json'}

while 1:

    active = []

    print("Performing inquiry...")
    nearby_devices = bluetooth.discover_devices(duration=5, lookup_names=True,
                                            flush_cache=True, lookup_class=False)

    for addr, name in nearby_devices:
        try:
            print("   {} - {}".format(addr, name))
            active.append(name)
        except UnicodeEncodeError:
            print("   {} - {}".format(addr, name.encode("utf-8", "replace")))
            active.append(name.encode("utf-8", "replace"))

    if len(active) > 0:
        data = json.dumps({'message':'|'.join(active)})
    else:
        data = json.dumps({'message':''})

    print(data)

    response = requests.put('http://localhost:8080/api/board/message', data = data, headers = headers)

    time.sleep(15)