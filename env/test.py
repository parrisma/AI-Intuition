"""
Simple test to validate the install of the python libraries.
"""

#
# Check Imports.
#
try:
    import tensorflow as tf
    from tensorflow import keras
    import numpy as np

    print("Tensor flow version [{}] & Keras import OK".format(tf.__version__))
except Exception as e:
    print("Failed to import tensorflow & Keras libraries, error: {}".format(str(e)))
    exit(-1)

try:
    from kafka import KafkaConsumer
    from kafka import KafkaProducer

    print("Kafka import OK")
except Exception as e:
    print("Failed to import Kafka libraries, error: {}".format(str(e)))
    exit(-1)


#
# Check TF & Keras actually runs
#
def tf_check() -> int:
    res = 1
    try:
        print(tf.reduce_sum(tf.random.normal([1000, 1000])))
        res = 0
    except Exception as e:
        print("Failed run a simple Tensorflow statement with error :{}".format(str(e)))
    return res


def keras_check() -> int:
    x = np.random.rand(5000, 1) * (np.pi * 2.0)
    y = np.sin(x)
    model = tf.keras.Sequential()
    model.add(
        tf.keras.layers.Dense(units=25, activation="relu", input_dim=1))
    model.add(tf.keras.layers.Dense(units=50, activation="relu"))
    model.add(tf.keras.layers.Dense(units=1))
    optimizer = tf.keras.optimizers.RMSprop(0.001)
    model.compile(loss='mse', optimizer=optimizer, metrics=['accuracy'])
    model.summary()
    _ = model.fit(x, y, epochs=50, batch_size=32, verbose=2, validation_split=0.2)
    xe = np.random.rand(500, 1) * (np.pi * 2.0)
    ye = np.sin(xe)
    model.evaluate(xe, ye, verbose=2)
    return 0


if tf_check() != 0:
    exit(-1)

if keras_check() != 0:
    exit(-1)

#
# All checks passed - exit with Zero to indicate OK
exit(0)
