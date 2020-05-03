from kafka import KafkaProducer

if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=str.encode)
    for i in range(5000):
        msg = "Message Type 2 {}".format(i)
        producer.send('3142', value=msg)
        print(msg)
    producer.flush()
