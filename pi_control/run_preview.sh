#! /bin/bash
#
while true
do
	export DISPLAY=:0
	feh --geometry 320x240+0+500 --auto-reload --info "echo $HOSTNAME" /home/pi/Desktop/preview.jpg
done

