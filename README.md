# family-board-jyserver
try jyserver for Family Board

## issues

### not able to stop server process

helper with PowerShell

```PowerShell
Get-Process python | ?{$_.CommandLine -match "server.py$"} | Stop-Process -Force
```