#!/bin/sh

sudo chmod +x /etc/rc.local
sudo echo "#!/bin/sh -e
sudo bash -c '/home/pi/git_pull.sh'
echo 'running rc.local' > /tmp/rc_test.txt
exit 0" > /etc/rc.local
