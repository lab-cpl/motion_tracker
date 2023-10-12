#! /bin/sh

echo "pi ip: $1"

IP=$1
ID=$2

# delete remote sample folder
ssh pi@$IP "sudo rm -f /home/pi/100_samples/*"

# cp to sample folder
ssh pi@$IP "cd /home/pi/images; find . -name 'ID_"$ID"_*.jpg' | sort | tail -n 100 | xargs cp -t /home/pi/100_samples/"

# delete local sample folder
sudo rm -f /home/nicoluarte/raspberry_images/*jpg

# cp to local folder
rsync --progress pi@$IP:/home/pi/100_samples/*.jpg /home/nicoluarte/raspberry_images/
