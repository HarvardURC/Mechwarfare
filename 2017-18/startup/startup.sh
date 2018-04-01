#!/bin/sh

# move this file to /etc/init.d
# run `chmod 755 startup.sh` to make the script executable
# include sudo password in a text file "password.txt"

git pull
sudo -S chmod 666 /dev/ttyUSB0 < ~/password.txt

# add more of these (backgrounded with &) if you're using multiple processes

cd ~/Mechwarfare/2017-18/frontend
python3 webtest.py
