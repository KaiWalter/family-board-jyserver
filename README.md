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
