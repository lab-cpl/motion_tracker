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

# switch to X11
```
sudo raspi-config
advanced options
A6 Wayland
select X11
```

# make scripts autostart
```
mkdir /home/pi/.config/lxsession
mkdir /home/pi/.config/lxsession/LXDE-pi
cp /etc/xdg/lxsession/LXDE-pi/autostart /home/pi/.config/lxsession/LXDE-pi/
add following lines at the end of that file
@lxterminal -e python3 /home/pi/motion_tracker/scripts/picam.py
```

# basic procedure

- reboot pi
- wait for a terminal to open and the connection succesful message
- start your arduino program as usual
- test out 1 event and 1 nosepoke a folder should appear in pi desktop
- a preview of the previous event should appear in pi
