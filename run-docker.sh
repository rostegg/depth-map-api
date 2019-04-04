#!/bin/bash

clear

EX_PATH="$( cd "$(dirname "$0")" ; pwd -P )/docker-compose.yml"
read -e -p $'\e[32mRun as daemon? ("NO" by default):\e[0m ' DAEMON_MODE

if [ -z "$DAEMON_MODE" ]
then
    docker-compose -f $EX_PATH up 
else
    docker-compose -f $EX_PATH up -d 
fi