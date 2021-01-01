# family-board-jyserver

Try [jyserver](https://github.com/ftrias/jyserver) for Family Board on **Raspberry Pi Zero W**.

## to do list

- [x] check out lightweight browsers : stay with `chromium` and `matchbox` window manager
- [x] implement server logging / tracing
- [x] check how `jyserver` handles external POST / GET for receiving tokens etc. : not directly possible; added `Flask`
- [x] store access or refresh tokens from Microsoft / Google locally on server : https://github.com/Azure-Samples/ms-identity-python-webapp
- [ ] update calendar from `jyserver` in browser
- [ ] update image from `jyserver` in browser
- [ ] make configuration and token handling generic

## configure Outlook / Live calendar access

- https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
- select `Applications from personal account`
- new registration
- Only associate with personal account
- enter redirect URL - e.g. for local development & testing: http://localhost:8080/msatoken
- select AzureADandPersonalMicrosoftAccount



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

create `startAsJob.ps1` for local (Win10) testing

### Kweb as alternate browser

> rendering capabilities not compatible or sufficient for family board

### Kweb needs Py2 as default

https://linuxconfig.org/how-to-change-from-default-to-alternative-python-version-on-debian-linux

```sh
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.7 2
update-alternatives --list python
update-alternatives --config python
```

### epiphany as alternate browser

> was not able to get `epiphany-browser` working in application mode / with no titlebar etc.

> `jyserver` to browser communication was not working reliably

> `jyserver` + `epiphany-browser` was too resource intensive allowing almost no SSHing

## check for other ideas

https://dominik.debastiani.ch/2019/01/18/raspberry-pi-als-kiosk-pc-mit-browser/
https://www.raspberrypi.org/forums/viewtopic.php?t=40860

