#!/bin/sh

sudo chmod +x /etc/rc.local
sudo echo "sudo bash -c '/home/pi/git_pull.sh'
echo "running rc.local" > /tmp/rc_test.txt" > /etc/rc.local
