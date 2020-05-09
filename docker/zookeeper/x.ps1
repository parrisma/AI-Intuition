echo "Simple test for Kafka - try to list all topics"
winpty docker run -it --rm --network=host edenhill/kafkacat:1.5.0 -b localhost:9092 -L
echo "done"