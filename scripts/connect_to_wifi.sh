#!/bin/bash

# WiFi SSID and password
SSID="Depto 901"
PASSWORD="dw4yb26f"

# Path to wpa_supplicant.conf
WPA_CONF="/etc/wpa_supplicant/wpa_supplicant.conf"

# Check if wpa_supplicant.conf exists
if [ ! -f "$WPA_CONF" ]; then
  echo "Error: wpa_supplicant.conf not found., file created"
  touch /etc/wpa_supplicant/wpa_supplicant.conf
fi

# Generate the network block
NETWORK_BLOCK="
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
country=CL
network={
    ssid=\"$SSID\"
    psk=\"$PASSWORD\"
}
"

# Append the network block to wpa_supplicant.conf
echo "$NETWORK_BLOCK" | sudo tee -a "$WPA_CONF" > /dev/null

# Reconfigure wpa_supplicant
sudo wpa_cli -i wlan0 reconfigure

# Check connection status (optional)
sleep 5 # Wait a few seconds for the connection to establish
ifconfig wlan0 | grep "inet "

# Check connection to the internet (optional)
ping -c 3 google.com

echo "WiFi configuration applied."

exit 0
