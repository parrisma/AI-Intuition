#!/bin/bash

cd /opt/kafka || exit
./bin/kafka-server-start.sh ./config/server.properties

while true; do
sleep 10
done
