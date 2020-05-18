from kafka import KafkaProducer

if __name__ == "__main__":

    #
    # This assumes Kafka is running on a local docker container with Kafka exposed via a PortNode
    # you can find the port node by running the command
    # kubectl get service --namespace ai-intuition
    # Then look at the ports listed in the output e.g. below
    # NAME               TYPE        CLUSTER - IP    EXTERNAL - IP    PORT(S)             AGE
    # kafka - service    NodePort    10.106.133.71   < none >         9092: 31903 / TCP   8h
    #
    producer = KafkaProducer(bootstrap_servers=['localhost:9099'], value_serializer=str.encode)
    for i in range(5000):
        msg = "Message Type 2 {}".format(i)
        ack = producer.send('topic-3142', value=msg)
        print("Produce: {}".format(msg))
        producer.flush()
    print('Done')
