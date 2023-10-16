#! /bin/sh


IP=$1
ID=$2
DATE=$(date +"%Y-%m-%d %H:%M:%S")

# install opencv
#
# update
ssh -n -f pi@$IP "sudo apt-get update &&
	sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y &&
	pip3 install opencv-python --break-system-packages"

# allow legacy cam (DO NOT SKIP!)
ssh -n -f pi@$IP "sudo raspi-config nonint do_legacy 0"

# create folder in desktop with pi number on in
ssh -n -f pi@$IP "mkdir -p /home/pi/Desktop/$HOSTNAME"


