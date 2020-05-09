#!/bin/bash

cd /opt/kafka || exit

if [[ -z "${ZOOKEEPER_SERVER}" ]]; then
  echo -------------------Use default Zookeeper in server.properties -----------------
else
  echo -------------------Override ZooKeeper server----------------------
  sed "s/zookeeper-server:2181/${ZOOKEEPER_SERVER}/g" ./config/server.properties > ./config/new_sp
  mv ./config/new_sp ./config/server.properties
fi

./bin/kafka-server-start.sh ./config/server.properties
