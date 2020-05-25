 docker build -f .\Dockerfile-Jetson-PyEnv . -t parrisma/jetson-pyenv:1.0
 docker build -f .\Dockerfile-NodeJs . -t parrisma/ai-nodejs:1.0

 # docker node update --label-add kafka=true docker-desktop
 # docker node update --label-add zookeeper=true docker-desktop
 # docker stack deploy -c .\docker-compose-ai.yml kafka