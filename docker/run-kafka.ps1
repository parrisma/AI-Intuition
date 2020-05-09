docker network create ai-net
docker run -d --rm -h zookeeper-server --name zookeeper-server --network ai-net zookeeper-server:1.0
docker run -d --rm -h kafka-server --name kafka-server -p 9092:9092 --network ai-net -e ZOOKEEPER_SERVER=zookeeper-server:2181 kafka-server:1.0

docker run -it --rm --network=host edenhill/kafkacat:1.5.0 -b localhost:9092 -L