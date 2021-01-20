# Family Board - in Python with JyServer and Flask

Use [jyserver](https://github.com/ftrias/jyserver) and [Flask](https://palletsprojects.com/p/flask/) for Family Board on **Raspberry Pi Zero W**.

## configure Microsoft Graph / Outlook / Live calendar access

- https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
- select `Applications from personal account`
- new registration
- click `Only associate with personal account`
- enter name
- select `Accounts in any organizational directory (Any Azure AD directory - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)`
- enter redirect URL - e.g. for local development & testing: http://localhost:8080/msgtoken
- add API permissions `Microsoft.Graph / delegated`
  * Calendars.Read
  * Files.Read.All
- create a script and set environment variables before starting `server.py`
  * MSG_CLIENT_ID
  * MSG_CLIENT_SECRET
  * MSG_AUTHORITY
- optionally set
  * MSG_CALENDAR_PATTERN : a Regex pattern selecting the names of calendars the above application has access to / can be checked with `/v1.0/me/calendars` in [Graph Explorer](https://developer.microsoft.com/en-us/graph/graph-explorer)
- when started login to MS account with http://localhost:8080/login
- a token that will be refreshed automatically is then stored on servers filesystem - `MSG_CACHE_FILE` application configuration setting

> after putting sensitive values in `.vscode/launch.json` it makes sense to exclude this file from __git commit__ with `git update-index --assume-unchanged .vscode/launch.json`

## configure Google Calendar API

https://developers.google.com/calendar

- Enable the Google Calendar API / create new project name
- configure OAuth client - Web server
- redirect URL : http://localhost:8080/googletoken
- create a script and set environment variables before starting `server.py`
  * GOOGLE_CLIENT_ID
  * GOOGLE_CLIENT_SECRET
- add `export OAUTHLIB_INSECURE_TRANSPORT=1` to allow authentication client w/o https
- when started login to Google account with http://localhost:8080/login
- a token that will be refreshed automatically is then stored on servers filesystem - `MSG_CACHE_FILE` application configuration setting

### configure locale

To show calendar events with local month and day designations, a locale can be set. Before using a locale in environment variable `MSG_LOCALE` it needs to be setup on Linux / Raspbian / Codespaces

```sh
sudo locale-gen de_DE.UTF-8
```

now `MSG_LOCALE` can be set (in the script which starts `server.py`)

```sh
export MSG_LOCALE=de_DE.utf8
```

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

### place a status

place a status that will be displayed with the next cycle; does not invoke a refresh

```PowerShell
Invoke-RestMethod -Method Put -Uri http://localhost:8080/api/board/status -ContentType "application/json" -body '{"status":"Family present"}'
```

---

## hints

### activate virtual environment with bash

```sh
source .venv/bin/activate
```

from https://docs.python.org/3/library/venv.html

---

### add log clean up

```sh
sudo nano /etc/logrotate.d/family-board
```

insert:
```
/home/pi/family-board-jyserver/family-board.log {
  rotate 3
  daily
  compress
  missingok
  notifempty
}
```


## issues

### pip install pybluez

in case of an `error: Microsoft Visual C++ 14.0 or greater is required`

- install with `winget install Microsoft.VisualStudio.BuildTools`
- modify installation - add C++ build tools - according to https://wiki.python.org/moin/WindowsCompilers

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

https://blog.gordonturner.com/2020/06/30/raspberry-pi-full-screen-browser-2020-05-27-raspios-buster/
https://dominik.debastiani.ch/2019/01/18/raspberry-pi-als-kiosk-pc-mit-browser/
https://www.raspberrypi.org/forums/viewtopic.php?t=40860


---

Any questions? [@ancientitguy](https://twitter.com/ancientitguy)