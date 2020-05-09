#!/bin/bash

cd /opt/kafka || exit

if [[ -z "${ZOOKEEPER_SERVER}" ]]; then
  echo -------------------Use default Zookeeper in server.properties -----------------
else
  echo -------------------Override ZooKeeper server----------------------
  sed "s/zookeeper-server:2181/${ZOOKEEPER_SERVER}/" ./config/server.properties > ./config/new_sp
  mv ./config/new_sp ./config/server.properties
fi

if [[ -z "${KAFKA_EXTERNAL}" ]]; then
  echo -------------------Remove EXTERNAL listener from server.properties -----------------
  sed "s/,EXTERNAL://123.456.789.123.:99999//" ./config/server.properties > ./config/new_sp
else
  echo -------------------Override EXTERNAL listener----------------------
  sed "s/EXTERNAL:\/\/123.456.789.123.:99999/EXTERNAL:\/\/${KAFKA_EXTERNAL}/" ./config/server.properties > ./config/new_sp
  mv ./config/new_sp ./config/server.properties
fi

if [[ -z "${KAFKA_PLAINTEXT}" ]]; then
  echo -------------------Use default listener in server.properties -----------------
else
  echo -------------------Override PLAINTEXT listener----------------------
  sed "s/PLAINTEXT:\/\/localhost:9092/PLAINTEXT:\/\/${KAFKA_PLAINTEXT}/" ./config/server.properties > ./config/new_sp
  mv ./config/new_sp ./config/server.properties
fi

./bin/kafka-server-start.sh ./config/server.properties

while true; do
sleep 10
done
