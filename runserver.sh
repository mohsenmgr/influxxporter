#!/bin/bash
HOST="YOUR_HOST"
USERNAME="YOUR_USERNAME"
PASSWORD="YOUR_PASSWORD"
SCRIPT=`cat script.sh`

echo -e "$ii Copying webserver into ${HOST}:/home/sachim.admin/tera4energyinfluxbackuptool \n"
sshpass -p "${PASSWORD}" ssh "$USERNAME"@"${HOST}" "rm -rf /home/sachim.admin/tera4energyinfluxbackuptool && mkdir /home/sachim.admin/tera4energyinfluxbackuptool"
sshpass -p "${PASSWORD}" scp -r "/mnt/c/proje/mossserver/tera4energyinfluxbackuptool" "${USERNAME}@${HOST}:/home/sachim.admin"
sshpass -p "${PASSWORD}" ssh "$USERNAME"@"${HOST}" "${SCRIPT}"

