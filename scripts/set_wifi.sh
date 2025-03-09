#!/bin/sh

sudo echo 'auto lo
iface lo inet loopback' > /etc/network/interfaces
