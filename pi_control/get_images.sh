#! /bin/sh


IP=$1
ID=$2
# does not need to be precise only to get roughly day and hour
# real sync is at ms level with arduino sendin timestamps
DATE=$(date +"%Y-%m-%d %H:%M:%S")

echo $FOLDER_NAME

ssh -n -f pi@$IP "mkdir -p /home/pi/scripts"
rsync -a /home/nicoluarte/repos_sync/motion_tracker/pi_control/get_images_sync.py pi@$IP:/home/pi/scripts/
rsync -a /home/nicoluarte/repos_sync/motion_tracker/pi_control/run_preview.sh pi@$IP:/home/pi/scripts/
ssh -n -f pi@$IP "chmod +x /home/pi/scripts/get_images_sync.py"
ssh -n -f pi@$IP "chmod +x /home/pi/scripts/run_preview.sh"
ssh -n -f pi@$IP "sudo date -s '$DATE'"
ssh -n -f pi@$IP "cd /home/pi/scripts; nohup python3 get_images_sync.py $ID > /home/pi/scripts/nohup.out 2>&1 &"
# run terminal to see lickometer output
ssh -n -f pi@$IP "rxvt --geometry 100x100+1060+0 -e sh -c 'tail -F /home/pi/scripts/nohup.out; bash'"
