#!/bin/bash

cd /opt/zookeeper || exit
./bin/zkServer.sh start-foreground
