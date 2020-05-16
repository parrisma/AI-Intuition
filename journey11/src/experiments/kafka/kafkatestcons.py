from kafka import KafkaConsumer

if __name__ == "__main__":
    #
    # This assumes Kafka is running on a local docker container with Kafka exposed via a PortNode
    # you can find the port node by running the command
    # kubectl get service --namespace ai-intuition
    # Then look at the ports listed in the output e.g. below
    # NAME               TYPE        CLUSTER - IP    EXTERNAL - IP    PORT(S)             AGE
    # kafka - service    NodePort    10.106.133.71   < none >         9092: 31903 / TCP   8h
    #
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092', auto_offset_reset='earliest')
    consumer.subscribe(['topic-kafka-test']) # ['topic-3142'])
    for message in consumer:
        print("Consumer: {}".format(message))
