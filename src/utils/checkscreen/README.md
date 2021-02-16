## setup required

- `raspi2png` - https://github.com/AndrewFromMelbourne/raspi2png#simple-install
- Python 3 with `PIL` library installed to evaluate color of captured screen `pip install -r requirements --upgrade requirements.txt`
- `xdotool` to refresh Chromium page

## cron

```
# m h  dom mon dow   command
*/1 *   *   *   * /home/pi/family-board-jyserver/utils/checkscreen/checkscreen.sh >> /home/pi/checkscreen.log 2>&1
```

## add log clean up

```sh
sudo nano /etc/logrotate.d/family-board-checkscreen
```

insert:
```
/home/pi/checkscreen.log {
  rotate 3
  daily
  compress
  missingok
  notifempty
}
```

## view captured screen in ASCII

```
sudo apt-get install caca-utils
cacaview screen.png
```

https://ozzmaker.com/view-images-as-ascii-in-the-terminal-on-a-raspberry-pi/
