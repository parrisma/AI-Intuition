#!/bin/bash

cd /opt/kafka || exit

if [[ -z "${ZOOKEEPER_SERVER}" ]]; then
  echo -------------------Use default server.properties -----------------
else
  echo -------------------Override ZooKeeper server----------------------
  sed "s/zookeeper-server:2181/${ZOOKEEPER_SERVER}/" ./config/server.properties > ./config/new_sp
  mv ./config/new_sp ./config/server.properties
fi

./bin/kafka-server-start.sh ./config/server.properties

while true; do
sleep 10
done
