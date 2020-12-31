# family-board-jyserver

Try [jyserver](https://github.com/ftrias/jyserver) for Family Board.

## hints

activate virtual environment with bash

```sh
source .venv/bin/activate
```

from https://docs.python.org/3/library/venv.html

## issues

### not able to stop server process

helper with PowerShell

```PowerShell
Get-Process python | ?{$_.CommandLine -match "server.py$"} | Stop-Process -Force
```

## check for other ideas

https://dominik.debastiani.ch/2019/01/18/raspberry-pi-als-kiosk-pc-mit-browser/
https://www.raspberrypi.org/forums/viewtopic.php?t=40860

## Kweb needs Py2 as default

https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux

```sh
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
update-alternatives --list python
update-alternatives --config python
```