#! /bin/bash
#
while true
do
	export DISPLAY=:0
	feh --auto-reload --info "echo $HOSTNAME" /home/pi/Desktop/preview.jpg
done

