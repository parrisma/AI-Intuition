import logging
import unittest
import numpy as np
from typing import List, ByteString
from kafka import KafkaProducer
from kafka import KafkaConsumer
from journey11.src.experiments.protokafka.protocopy import ProtoCopy
from journey11.src.experiments.protokafka.task import Task
from journey11.src.experiments.protokafka.pb_task_pb2 import PBTask
from journey11.src.experiments.protokafka.pb_message1_pb2 import PBMessage1
from journey11.src.experiments.protokafka.message1 import Message1
from journey11.src.experiments.protokafka.state import State
from journey11.src.experiments.protokafka.gibberish import Gibberish
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.loggingsetup import LoggingSetup


class KafkaTestProducer:

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092',
                                      value_serializer=None)
        return

    def pub(self, topic: str, msg: str) -> None:
        _ = self.producer.send(topic, value=msg)
        self.producer.flush()
        return


class KafkaTestConsumer:

    def __init__(self, topics: List[str]):
        self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                      group_id="grp-1",
                                      auto_offset_reset='earliest')
        self.consumer.subscribe(topics)
        return

    def sub(self):
        msg = self.consumer.poll(timeout_ms=500, max_records=1)
        if len(msg) > 0:
            return list(msg.values())[0][0].value
        return None


class TestProtoKafka(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def test_simple_class(self):
        pc = ProtoCopy()
        pc.register(object_type=Task, proto_buf_type=PBTask)

        task = Task(task_name="Task-3142", task_id=3142)

        byte_str = pc.serialize(task)
        self.assertEqual(b'\n\tTask-3142\x10\xc6\x18', byte_str)

        task_deserialized = pc.deserialize(byte_str, Task)
        self.assertEqual(task, task_deserialized)

        return

    def test_nested_class(self):
        pc = ProtoCopy()
        pc.register(object_type=Message1, proto_buf_type=PBMessage1)

        message1 = Message1(field=Gibberish.more_gibber(),
                            state=State.S2,
                            tasks=[Task(task_name="Task-1", task_id=1), Task(task_name="Task-2", task_id=2)])

        message1_serialized = pc.serialize(message1)
        m1_b = bytes(message1_serialized).decode(encoding='utf-8')
        message1_deserialized = pc.deserialize(m1_b, Message1)
        self.assertEqual(message1_deserialized, message1)
        return

    def test_class_over_kafka(self):
        # Start the Kafka service with the /AI-Intuition/docker/run-kafka.ps1
        # you will need a docker environment (or Docker Desktop on windows). The containers are on dockerhub
        # but they can also be built locally as the Dockerfile for them are on the same directory as the run
        # script - where there is also the build script for the containers.
        logging.info("Run large scale test Class over Kafka")
        pc = ProtoCopy()
        pc.register(object_type=Message1, proto_buf_type=PBMessage1)

        kafka_topic = UniqueRef().ref  # Unique topic to ensure queue is empty
        logging.info("Setting up to use topic: {}".format(kafka_topic))
        kafka_pub = KafkaTestProducer()
        kafka_con = KafkaTestConsumer([kafka_topic])

        # Push Random Messages
        num_msg = 1000
        states = [State.S1, State.S2, State.S3]
        state_choice = np.random.choice(3, num_msg)
        num_tasks = 1 + np.random.choice(50, num_msg)

        messages = dict()
        for i in range(num_msg):
            task_list = list()
            for j in range(num_tasks[i]):
                rint = int(np.random.randint(10000, size=1)[0])
                task_list.append(Task(task_name="Task-{}".format(rint), task_id=rint))

            msg = Message1(field="{}-{}".format(np.random.random() * 10000, Gibberish.more_gibber()),
                           state=states[state_choice[i]],
                           tasks=task_list)
            messages[msg.field] = msg
            kafka_pub.pub(topic=kafka_topic, msg=pc.serialize(msg))
            logging.info("Sent message : {}".format(msg.field[0:100]))

        rx_msg = ""
        while rx_msg is not None:
            rx_msg = kafka_con.sub()
            if rx_msg is not None:
                rx_deserialized = pc.deserialize(rx_msg, Message1)
                expected = messages[rx_deserialized.field]
                self.assertEqual(expected, rx_deserialized)
                logging.info("Rx'ed and passed message :{}".format(expected.field[0:100]))

        return


if __name__ == "__main__":
    unittest.main()
