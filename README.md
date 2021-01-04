# family-board-jyserver

Use [jyserver](https://github.com/ftrias/jyserver) and [Flask](https://palletsprojects.com/p/flask/) for Family Board on **Raspberry Pi Zero W**.

## to do list

- [x] check out lightweight browsers : stay with `chromium` and `matchbox` window manager
- [x] implement server logging / tracing
- [x] check how `jyserver` handles external POST / GET for receiving tokens etc. : not directly possible; added `Flask`
- [x] store access or refresh tokens from Microsoft / Google locally on server : https://github.com/Azure-Samples/ms-identity-python-webapp
- [x] update calendar from `jyserver` in browser
- [x] update image from `jyserver` in browser
- [ ] make configuration and token handling generic

## configure locale

before using a locale in environment variable `LOCALE` it needs to be setup on Linux / Raspbian / Codespaces

```sh
sudo locale-gen de_DE.UTF-8
```

now `LOCALE` can be set

```sh
export LOCALE=de_DE.utf8
```

## configure Outlook / Live calendar access

- https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
- select `Applications from personal account`
- new registration
- click `Only associate with personal account`
- enter name
- select `Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)`
- enter redirect URL - e.g. for local development & testing: http://localhost:8080/msatoken
- add API permissions `Microsoft.Graph / delegated`
  * Calendars.Read
  * Files.Read.All

## API access

### refresh board

trigger a refresh for the board (image + calendar) with the next cycle

```PowerShell
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/board/refresh
```

### place a message

place a message that will be displayed with the next cycle; also invokes a refresh

```PowerShell
Invoke-RestMethod -Method Put -Uri http://localhost:8080/api/board/message -ContentType "application/json" -body '{"message":"Hello, world!"}'
```

---

## hints

activate virtual environment with bash

```sh
source .venv/bin/activate
```

from https://docs.python.org/3/library/venv.html

---

## issues

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


---

Any questions? [@ancientitguy](https://twitter.com/ancientitguy)