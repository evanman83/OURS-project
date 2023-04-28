#!/bin/bash

now="$(date)"
printf "\nBoot time: %s\n" "$now"

echo "Wait for qmi_wwan to load, then remove it (max 20 sec)"
i=1
while [ $i -lt 20 ]
do
  echo "Checking"
  modules=$(lsmod)
  if [[ "$modules" == *"qmi_wwan"* ]]; then
    echo "Removing qmi_wwan"
    sudo rmmod qmi_wwan
    break
  fi
  i=`expr $i + 1`
  sleep 1
done

echo "Installing simcom_wwan"
sudo insmod /home/evan/SIM7600_NDIS/simcom_wwan.ko
sleep 3
echo "Turning on wwan0"
sudo ifconfig wwan0 up
sleep 3
echo "Activating data on sim"
sudo echo -e 'AT$QCRMCALL=1,1\r\n' >> /dev/ttyUSB2
sleep 5
echo "Connecting to web"
sudo udhcpc -i wwan0

