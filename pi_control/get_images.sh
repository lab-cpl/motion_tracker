#! /bin/sh


IP=$1
ID=$2
DATE=$(date +"%Y-%m-%d %H:%M:%S")
FOLDER_NAME=$(date +"%Y-%m-%d_%H_%M")

echo $FOLDER_NAME

ssh -n -f pi@$IP "mkdir -p /home/pi/scripts"
#ssh -n -f pi@$IP "mkdir -p /home/pi/images/$FOLDER_NAME"
rsync -a /home/nicoluarte/repos_sync/motion_tracker/pi_control/get_images.py pi@$IP:/home/pi/scripts/
ssh -n -f pi@$IP "chmod +x /home/pi/scripts/get_images.py"
ssh -n -f pi@$IP "sudo date -s '$DATE'"
ssh -n -f pi@$IP "cd /home/pi/scripts; nohup python3 get_images.py $ID > /dev/null 2>&1 &"
