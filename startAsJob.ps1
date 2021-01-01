
$j = Start-Job -ScriptBlock { python ./server.py -o family-board.log -a 0.0.0.0 -p 8080 }

Start-Sleep -Seconds 1

Start-Process "http://localhost:8080"

Read-Host "Hit <-´ to stop"

$j | Stop-Job -PassThru | Remove-Job -Force