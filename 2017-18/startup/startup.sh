#!/bin/sh

# run `chmod 755 startup.sh` to make the script executable
# include sudo password in a text file "~/password.txt"

# To add the script on startup, do:
# `crontab -e`
# add the line:
# `@reboot ~/Mechwarfare/2017-18/startup/startup.sh &`
# save the file

cd ~/Mechwarfare/2017-18/frontend
git pull
sudo -S chmod 666 /dev/ttyUSB0 < ~/password.txt

# restart the server if it crashes
while true; do python3 webtest.py; done
