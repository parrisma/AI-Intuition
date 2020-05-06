docker system prune --force
docker network rm kafka-net
docker network create --attachable kafka-net
