docker network create ai-net
docker run -d --rm -h zookeeper-server --name zookeeper-server --network ai-net zookeeper-server:1.0
docker run -d --rm -h kafka-server --name kafka-server -p 9092:9092 --network ai-net kafka-server:1.0

