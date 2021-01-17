import os
import json
import requests

from fritzconnection.lib.fritzhosts import FritzHosts

ADDRESS = os.environ['FRITZ_HOST']  # FritzBox
PASSWORD = os.environ['FRITZ_PWD']  # password
SCAN_HOSTS = os.environ['FRITZ_SCAN_HOSTS'].split(
    ',')  # CSV of wifi hosts to scan for


def hosts():
    active_hosts = []
    fh = FritzHosts(address=ADDRESS, password=PASSWORD)
    hosts = fh.get_hosts_info()
    for index, host in enumerate(hosts, start=1):
        # print(f"{host['name']:<28} {host['status']}")
        if host['status']:
            if host['name'] in SCAN_HOSTS:
                active_hosts.append(host['name'])

    return active_hosts


if __name__ == '__main__':
    active = hosts()

    if len(active) > 0:
        data = {'status': ' | '.join(active)}
    else:
        data = {'status': ''}

    headers = {'Content-Type': 'application/json'}
    payload = json.dumps(data)

    print(data)
    response = requests.put(
        'http://localhost:8080/api/board/status', data=data, headers=headers)
