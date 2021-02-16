## setup

- `pip install -r requirements --upgrade requirements.txt`

### add environment variables to `.profile`

```
...
# secrets
export FRITZ_HOST=fritz.box
export FRITZ_PWD=fritzboxpassword
export FRITZ_SCAN_HOSTS=phone1,phone2,tablet
```

## cron

```
# m h  dom mon dow   command
*/5 *   *   *   * . /home/pi/.profile; /home/pi/family-board-jyserver/utils/fritzbox/checkpresence.sh >> /home/pi/checkpresence.log 2>&1
```

## add log clean up

```sh
sudo nano /etc/logrotate.d/family-board-checkpresence
```

insert:
```
/home/pi/checkpresence.log {
  rotate 3
  daily
  compress
  missingok
  notifempty
}
```