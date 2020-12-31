
$j = Start-Job -ScriptBlock { python ./server.py }

Start-Sleep -Seconds 1

Start-Process "http://localhost:8080"

Read-Host "Hit <-´ to stop"

$j | Stop-Job -PassThru | Remove-Job -Force