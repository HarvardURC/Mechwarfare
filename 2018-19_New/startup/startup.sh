#!/bin/sh

# run `chmod 755 startup.sh` to make the script executable
# include sudo password in a text file "~/password.txt"

# To add the script on startup, do:
# `crontab -e`
# add the line:
# `@reboot ~/Downloads/Mechwarfare/2018-19_New/startup/startup.sh &`
# sagit pull

cd ~

sudo ./hub-ctrl -h 0 -P 2 -p 0
sleep 5
sudo ./hub-ctrl -h 0 -P 2 -p 1
sleep 2
sudo -S chmod 666 /dev/ttyUSB0 < ~/password.txt &> passErr.txt 

echo ok >> log.txt

# restart the server if it crashes
python3 /home/pi/Downloads/Mechwarfare/2018-19_New/frontend/webtest.py < /dev/pts/0 &> err.txt; date >> log.txt; echo reboot >> log.txt;  done
