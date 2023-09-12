#!/bin/bash
hostname=$(uname -n)
echo -e "hostname: $hostname \n"
cd /home/sachim.admin/tera4energyinfluxbackuptool
echo -e "Start Webserver \n"
gunicorn -w 1 -b 0.0.0.0:8080 app:app
exit
