# update and install git

```console
sudo apt-get update
sudo apt-get install git
```

# clone repository
```console
git clone https://github.com/lab-cpl/motion_tracker.git
```

# allow for script execution
```console
chmod +x /home/pi/motion_tracker/scripts/*.sh
```

# run auto_run.sh
```console
sudo bash /home/pi/motion_tracker/scripts/auto_run.sh
```

# set wifi
```console
sudo bash /home/pi/motion_tracker/scripts/set_wifi.sh
```

# connect to wifi
```
sudo raspi-config
```
System options -> Wireless LAN -> set SSID and PASSWORD
```
sudo reboot
```

# install python picamera2
```
sudo apt-get full-upgrade
libcamera-hello --list-cameras
```
this should list the IR camera, something like "SGBRG10_CSI2P"
