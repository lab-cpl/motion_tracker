#!/bin/bash
#
#

echo -n "SET_HOST or POWEROFF or REBOOT or START or STOP recording + animal IDs: "
read -r C ID1 ID2 ID3 ID4

PIARRAY=( pi1 pi2 pi3 pi4 )
IDARRAY=( $ID1 $ID2 $ID3 $ID4 )

case $C in

	START)
		for i in "${!PIARRAY[@]}"
		do
			echo "saving frames in ${PIARRAY[i]} with ID: ${IDARRAY[i]}"
			bash get_images.sh ${PIARRAY[i]} ${IDARRAY[i]}
		done
		;;

	STOP)
		for i in "${!PIARRAY[@]}"
		do
			echo "stopin frames in ${PIARRAY[i]} with ID: ${IDARRAY[i]}"
			ssh ${PIARRAY[i]} "pkill python3"
			ssh ${PIARRAY[i]} "pkill rxvt"
		done
		;;

	REBOOT)
		for i in "${!PIARRAY[@]}"
		do
			echo "reboot in ${PIARRAY[i]} with ID: ${IDARRAY[i]}"
			ssh ${PIARRAY[i]} "sudo reboot"
		done
		;;

	POWEROFF)
		for i in "${!PIARRAY[@]}"
		do
			echo "poweroff in ${PIARRAY[i]} with ID: ${IDARRAY[i]}"
			ssh ${PIARRAY[i]} "sudo poweroff"
		done
		;;

	SET_HOST)
		for i in "${!PIARRAY[@]}"
		do
			echo "changing host in ${PIARRAY[i]} with ID: ${IDARRAY[i]}"
			ssh ${PIARRAY[i]} "mkdir -p /home/pi/Desktop/${PIARRAY[i]}"
		done
		;;
esac

