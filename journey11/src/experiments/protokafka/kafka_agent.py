import logging
import numpy as np
import time
import argparse
from typing import List
from kafka import KafkaProducer
from kafka import KafkaConsumer
from src.lib.protocopy import ProtoCopy
from journey11.src.experiments.protokafka.task import Task
from journey11.src.experiments.protokafka.pb_message1_pb2 import PBMessage1
from journey11.src.experiments.protokafka.message1 import Message1
from journey11.src.experiments.protokafka.state import State
from src.test.gibberish.gibberish import Gibberish
from src.lib.aitrace.trace import Trace


class KafkaTestProducer:

    def __init__(self,
                 topic: str,
                 server: str):
        self.producer = KafkaProducer(bootstrap_servers=server,
                                      value_serializer=None)
        self._topic = topic
        logging.info("Kafka Producer to topic: {}".format(self._topic))
        self._pc = ProtoCopy()
        self._pc.register(native_object_type=Message1, proto_buf_type=PBMessage1)
        return

    def pub(self, topic: str, msg: str) -> None:
        _ = self.producer.send(topic, value=msg)
        self.producer.flush()
        return

    def run(self):
        while True:
            num_msg = np.random.randint(250)
            logging.info("Publisher sending message burst of {}".format(num_msg))
            states = [State.S1, State.S2, State.S3]
            state_choice = np.random.choice(3, num_msg)
            num_tasks = 1 + np.random.choice(50, num_msg)

            for i in range(num_msg):
                task_list = list()
                for j in range(num_tasks[i]):
                    rint = int(np.random.randint(10000, size=1)[0])
                    task_list.append(Task(task_name="Task-{}".format(rint), task_id=rint))

                msg = Message1(field="{}-{}".format(np.random.random() * 10000, Gibberish.more_gibber()),
                               state=states[state_choice[i]],
                               tasks=task_list)
                self.pub(topic=self._topic, msg=self._pc.serialize(msg))
                logging.info("Sent message : {}".format(msg.field[0:100]))
            sleep_sec = np.random.randint(10)
            logging.info("Producer paused for {} seconds".format(str(sleep_sec)))
            time.sleep(sleep_sec)


class KafkaTestConsumer:

    def __init__(self,
                 topics: List[str],
                 server: str,
                 group_id: str):
        self.consumer = KafkaConsumer(bootstrap_servers=server,
                                      group_id=group_id,
                                      auto_offset_reset='earliest')
        self.consumer.subscribe(topics)
        self._pc = ProtoCopy()
        self._pc.register(native_object_type=Message1, proto_buf_type=PBMessage1)
        return

    def sub(self):
        msg = self.consumer.poll(timeout_ms=500, max_records=1)
        if len(msg) > 0:
            return list(msg.values())[0][0].value
        return None

    def run(self):
        while True:
            rx_msg = ""
            logging.info("checking for messages")
            while rx_msg is not None:
                rx_msg = self.sub()
                if rx_msg is not None:
                    rx_deserialized = self._pc.deserialize(rx_msg, Message1)
                    logging.info("Rx'ed :{}".format(str(rx_deserialized)))
            logging.info("No messages sleeping for 5 seconds")
            time.sleep(5)


class Do:

    def __init__(self):
        args = self._args()
        self._producer = args.producer
        self._consumer = args.consumer
        self._group_id = args.consumer_group
        self._server = args.server
        self._topic = args.topic

        if self._producer and self._consumer:
            logging.fatal("Cannot be both a producer and consumer at the same time")

        if not self._producer and not self._consumer:
            logging.fatal("Must be either a producer or consumer")

        if self._topic is None or len(self._topic) == 0:
            logging.fatal("Topic must be a non zero length string : {}".format(self._topic))

        logging.info(str(self))

        return

    def __str__(self):
        res = ""
        if self._consumer:
            res = "Consumer talking to server [{}] from group [{}] on topic [{}]".format(self._server, self._group_id,
                                                                                         self._topic)
        else:
            res = "Producer talking to server [{}] on topic [{}]".format(self._server, self._topic)
        return res

    def run(self):
        if self._consumer:
            logging.info("Agent starting as Consumer")
            kafka_con = KafkaTestConsumer(topics=[self._topic],
                                          group_id=self._group_id,
                                          server=self._server)
            kafka_con.run()
        else:
            logging.info("Agent starting as Producer")
            kafka_pub = KafkaTestProducer(topic=self._topic,
                                          server=self._server)
            kafka_pub.run()

        logging.info("Kafka agent done, exiting")
        return

    @classmethod
    def _args(cls):
        parser = argparse.ArgumentParser()
        parser.add_argument("--producer", help="Start as a Kafka Producer", default=False, action='store_true')
        parser.add_argument("--consumer", help="Start as a Kafka Consumer", default=False, action='store_true')
        parser.add_argument("--server", help="The Kafka host:port e.g. localhost:9092", default='localhost:9092')
        parser.add_argument("--consumer_group", help="Consumer group id e.g. grp-1", default='grp-1')
        parser.add_argument("--topic", help="Kafka Topic", default=None)
        return parser.parse_args()


if __name__ == "__main__":
    Trace()
    logging.info("Kafka agent starting")
    Do().run()
    logging.info("Kafka agent exit")
    exit(0)
