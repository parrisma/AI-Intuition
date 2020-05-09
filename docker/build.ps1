 docker build -f .\Dockerfile-Ubuntu-Java . -t parrisma/ubuntu-java:1.0 --no-cache
 docker build -f .\Dockerfile-ZooKeeper . -t parrisma/zookeeper:1.0 --no-cache
 docker build -f .\Dockerfile-ZooKeeper-server . -t parrisma/zookeeper-server:1.0 --no-cache
 docker build -f .\Dockerfile-Kafka . -t parrisma/kafka:1.0 --no-cache
 docker build -f .\Dockerfile-Kafka-server . -t parrisma/kafka-server:1.0 --no-cache
