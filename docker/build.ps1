 docker build -f .\Dockerfile-Ubuntu-Java . -t parrisma/ubuntu-java:1.0 --no-cache
 docker build -f .\Dockerfile-ZooKeeper . -t parrisma/zookeeper:1.0 --no-cache
 docker build -f .\Dockerfile-ZooKeeper-server . -t parrisma/zookeeper-server:1.0 --no-cache
 docker build -f .\Dockerfile-Kafka . -t parrisma/kafka:1.0 --no-cache
 docker build -f .\Dockerfile-Kafka-server . -t parrisma/kafka-server:1.0 --no-cache
 docker build -f .\Dockerfile-PyEnv . -t parrisma/py-env:1.0

 cd "C:\Program Files\Docker\Docker\"
 ./DockerCli.exe -SwitchDaemon

  //d/Dev/devroot:/var/data

 docker run -it -v //d/Dev/devroot:/var/data parrisma/py-env:1.0

 protoc --proto_path=. --python_out=. ./state.proto