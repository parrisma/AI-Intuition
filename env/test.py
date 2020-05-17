"""
Simple test to validate the install of the python libraries.
"""
try:
    import tensorflow as tf
    from tensorflow import keras

    print("Tensor flow & Keras import OK")
except Exception as e:
    print("Failed to import tensorflow & Keras libraries {}".format(str(e)))
    exit(-1)

try:
    from kafka import KafkaConsumer
    from kafka import KafkaProducer

    print("Kafka import OK")
except Exception as e:
    print("Failed to import Kafka libraries {}".format(str(e)))
    exit(-1)

exit(0)
