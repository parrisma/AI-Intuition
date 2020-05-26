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
    [string]$KafkaHost = $env:COMPUTERNAME,
    [string]$KafkaPort = "9092",
    [string]$DockerKafkaServer = "kafka-server",
    [String]$DockerKafkaPort = "19092",
    [string]$ZookeeperServer = "zookeeper-server",
    [string]$ZookeeperPort = "2181",
    [string]$DockerNetwork = "ai-net",
    [String]$Repository = "parrisma",
    [String]$KafkaVer = "1.0",
    [String]$ZookeeperVer = "1.0",
    [Switch]$StopOnly
)

. ..\..\ps1\BuildDockerFile.ps1

DockerNetworkCreate -NetworkName ai-net
DockerStopContainerByName -ContainerName ${ZookeeperServer}
DockerStopContainerByName -ContainerName ${DockerKafkaServer}
DockerPruneContainersAndImages

if ($StopOnly)
{
    exit
}

# Both of these images are on docker hub in public repositories parrisma/<>

Write-Output "Starting Zookeeper"
docker run -d --rm `
--hostname ${ZookeeperServer} --name ${ZookeeperServer} `
--network ${DockerNetwork} `
$Repository/$ZookeeperServer`:$ZookeeperVer

Write-Output "Wait for Zookeeper start"
Start-Sleep 5

Write-Output "Starting Kafka"

docker run `
-d --rm `
--hostname ${DockerKafkaServer} --name ${DockerKafkaServer} `
-p ${KafkaPort}:${KafkaPort} --network ${DockerNetwork} `
-e ZOOKEEPER_HOST="${ZookeeperServer}:${ZookeeperPort}" `
-e DOCKER_KAFKA_HOST="${DockerKafkaServer}" `
-e DOCKER_KAFKA_PORT="${DockerKafkaPort}" `
-e EXT_KAFKA_HOST="${KafkaHost}" `
-e EXT_KAFKA_PORT="${KafkaPort}" `
$Repository/kafka-server:$KafkaVer

Write-Output "Wait for Kafka start"
Start-Sleep 5

Write-Output "Done"
