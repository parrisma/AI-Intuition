$kf = docker ps --filter "name=kafka-server" -q
if ($kf) {
    echo "Stopping Kafka : $kf"
    docker stop $kf
    echo "Kafka stopped"
}


$zk = docker ps --filter "name=zookeeper-server" -q
if ($zk) {
    echo "Stopping Zookeeper : $zk"
    docker stop $zk
    echo "Zookeeper stopped"
}

$error.clear()
try { docker network inspect ai-net > $null}
catch {
    echo "ai-net does not exist, create"
    docker network create ai-net
}
if (!$error) {
echo "Docker network ai-net already exists, no need to create"
}

# Both of these images are on docker hub in public repositories

echo "Starting Zookeeper"
docker run -d --rm -h zookeeper-server --name zookeeper-server --network ai-net parrisma/zookeeper-server:1.0

echo "Starting Kafka"
docker run -d --rm -h kafka-server --name kafka-server -p 9092:9092 --network ai-net -e ZOOKEEPER_SERVER=zookeeper-server:2181 parrisma/kafka-server:1.0

echo "Wait for start"
sleep 5

echo "Simple test for Kafka - try to list all topics"
docker run -it --rm --network=host edenhill/kafkacat:1.5.0 -b localhost:9092 -L