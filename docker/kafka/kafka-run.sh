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

# Just for testing, so we can stop the current Kafka and fix settings etc
# without the container exiting.

# Un comment for testing, where Kafka fails to start and you want to see logs & restart with new settings
# docker exec -it <kafka container id> /bin/bash
#while true; do
#  sleep 10
#  echo Tick
#done