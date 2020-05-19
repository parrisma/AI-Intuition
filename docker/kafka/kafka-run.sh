#!/bin/bash

cd /opt/kafka || exit

if [[ -z "${ZOOKEEPER_SERVER}" ]]; then
  echo -------------------Use default Zookeeper in server.properties -----------------
else
  echo -------------------Override ZooKeeper server----------------------
sed "s/zookeeper-server:2181/${ZOOKEEPER_SERVER}/g" ./config/server.properties > ./config/new_sp
mv ./config/new_sp ./config/server.properties
fi

if [[ -z "${EXT_KAFKA_HOST}" ]] || [[ -z "${EXT_KAFKA_PORT}" ]]; then
  echo "ERROR: Script required environment variables EXT_KAFKA_HOST and EXT_KAFKA_PORT to be set"
  exit 1
fi

echo " Override the EXTERNAL Kafka listener and advertised listener : ${EXT_KAFKA_HOST}:${EXT_KAFKA_PORT}"
sed "s/EXT-KAFKA-HOST/${EXT_KAFKA_HOST}/g" ./config/server.properties > ./config/new_sp
mv ./config/new_sp ./config/server.properties
sed "s/EXT-KAFKA-PORT/${EXT_KAFKA_PORT}/g" ./config/server.properties > ./config/new_sp
mv ./config/new_sp ./config/server.properties

if [[ -z "${DOCKER_KAFKA_HOST}" ]] || [[ -z "${DOCKER_KAFKA_PORT}" ]]; then
  echo "ERROR: Script required environment variables DOCKER_KAFKA_HOST and DOCKER_KAFKA_PORT to be set"
  exit 1
fi

echo " Override the INTERNAL Kafka listener and advertised listener : ${DOCKER_KAFKA_HOST}:${DOCKER_KAFKA_PORT}"
sed "s/DOCKER-KAFKA-HOST/${DOCKER_KAFKA_HOST}/g" ./config/server.properties > ./config/new_sp
mv ./config/new_sp ./config/server.properties
sed "s/DOCKER-KAFKA-PORT/${DOCKER_KAFKA_PORT}/g" ./config/server.properties > ./config/new_sp
mv ./config/new_sp ./config/server.properties

exit 0