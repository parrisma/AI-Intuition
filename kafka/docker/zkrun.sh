#!/bin/bash

cd /opt/zookeeper || exit
./zkServer.sh start-foreground 2>&1 /var/log/zookeeper.log &