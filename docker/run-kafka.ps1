<#
  `-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-"`-._,-"`-._,-"`-._,-"`-._,-"`-._,-"`-._,
  * kafka_host
               : If not supplied we assume the discoverable hostname to use for the External Kafka listener is the
               : current host on which this script is being run. This is the server name injected into the
               : kafka server.properties file inside the kafka container (EXTERNAL)

  * kafka_port
               : If not supplied we assume the default kafka port for the External kafka listener. This is also
               : exposed as the same port inside the container.This is the server name injected into the
               : kafka server.properties file  inside the kafka container (EXTERNAL)

  * docker_kafka_server
               : The name to give to the docker container and also the hostname to assign the container inside
               : the conatiner network. This is also injected into the server.properties file used inside the
               : container to defined which server the kakfa brokers communicate over (INTERNAL)

  * docker_kafka_port
               : This is injected into the server used inside the Kafka server.properties on which the
               : kafka brokers communicate over (INTERNAL)

  * zookeeper_server
               : The name to give to the docker container in which the zookeeper server runs. This is also
               : the hostname given to this container on the docker network and the hostname injected
               : into the kafka server.properties files for where it finds zookeeper

  * zookeeper_port
               : This is *NOT* exposed as a conatiner port as zookeeper only needs to be visible over the
               : internal docker network. It is injected into the kafka server.properties files for where it
               : finds zookeeper

  * docker_network
               : The name of the docker (container) network to whcih the zookeeper and kafka containers with
               : both be attached. This will mean they can cooperate as a pair. If this network does not
               : exist it will be created. Default is 'ai-net'
   `-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-'"`-._,-"`-._,-"`-._,-"`-._,-"`-._,-"`-._,-"`-._,
#>

param (
    [string]$kafka_host = $env:COMPUTERNAME,
    [string]$kafka_port = "9092",
    [string]$docker_kafka_server = "kafka-server",
    [String]$docker_kafka_port = "19092",
    [string]$zookeeper_server = "zookeeper-server",
    [string]$zookeeper_port = "2181",
    [string]$docker_network = "ai-net"
 )

Write-Output "Stopping and restarting Kafka and Zookeeper Containers"

$kf = docker ps --filter "name=${docker_kafka_server}" -q
if ($kf) {
    Write-Output "Stopping Kafka [${docker_kafka_server}]: $kf"
    docker stop $kf
    Write-Output "Kafka container [${docker_kafka_server}] stopped"
}


$zk = docker ps --filter "name=${zookeeper_server}" -q
if ($zk) {
    Write-Output "Stopping Zookeeper [${zookeeper_server}] : $zk"
    docker stop $zk
    Write-Output "Zookeeper container [${zookeeper_server}] stopped"
}

$error.clear()
try { docker network inspect ${docker_network} > $null}
catch {
    Write-Output "Docker network ${docker_network} does not exist, creating"
    docker network create ${docker_network}
}
if (!$error) {
Write-Output "Docker network ${docker_network} already exists, no need to create"
}

# Both of these images are on docker hub in public repositories parrisma/<>

Write-Output "Starting Zookeeper"
docker run -d --rm `
-h ${zookeeper_server} --name ${zookeeper_server} `
--network ${docker_network} `
parrisma/zookeeper-server:1.0

Write-Output "Wait for Zookeeper start"
Start-Sleep 5

Write-Output "Starting Kafka"
$docker_kafka_server = "kafka-server"

docker run `
-d --rm `
--hostname ${docker_kafka_server} --name ${docker_kafka_server} `
-p ${kafka_port}:${kafka_port} --network ${docker_network} `
-e ZOOKEEPER_HOST="${zookeeper_server}:${zookeeper_port}" `
-e DOCKER_KAFKA_HOST="${docker_kafka_server}" `
-e DOCKER_KAFKA_PORT="${docker_kafka_port}" `
-e EXT_KAFKA_HOST="${kafka_host}" `
-e EXT_KAFKA_PORT="${kafka_port}" `
parrisma/kafka-server:1.0

Write-Output "Wait for Kafka start"
Start-Sleep 5

Write-Output "Done"

#Write-Output "Simple test for Kafka - try to list all topics"
#docker run -it --rm --network=host edenhill/kafkacat:1.5.0 -b ${docker_kafka_server}:${docker_kafka_port} -L