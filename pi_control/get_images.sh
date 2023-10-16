#! /bin/sh


IP=$1
ID=$2
DATE=$(date +"%Y-%m-%d %H:%M:%S")

echo $FOLDER_NAME

ssh -n -f pi@$IP "mkdir -p /home/pi/scripts"
rsync -a /home/nicoluarte/repos_sync/motion_tracker/pi_control/get_images.py pi@$IP:/home/pi/scripts/
ssh -n -f pi@$IP "chmod +x /home/pi/scripts/get_images.py"
ssh -n -f pi@$IP "sudo date -s '$DATE'"
ssh -n -f pi@$IP "cd /home/pi/scripts; nohup python3 get_images.py $ID > /dev/null 2>&1 &"
