#!/bin/sh

sudo chmod +x /etc/rc.local
sudo echo "sudo bash -c '/home/pi/git_pull.sh'" > /etc/rc.local
