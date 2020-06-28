import numpy as np
import unittest
import threading
import time
from typing import List, Tuple, Callable, Any
from datetime import datetime
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap
from journey11.src.lib.kpubsub.kpubsub import KPubSub
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.filestream import FileStream
from journey11.src.lib.kpubsub.kpsutil import KPSUtil
from journey11.src.lib.envboot.env import Env
from journey11.src.lib.envboot.env import EnvBuilder
from src.lib.envboot.runspec import RunSpec
from journey11.src.test.kpubsub.pb_message1_pb2 import PBMessage1
from journey11.src.test.kpubsub.pb_message2_pb2 import PBMessage2
from journey11.src.test.kpubsub.message2 import Message2
from journey11.src.test.kpubsub.message1 import Message1


class ConsumerListener:
    def __init__(self,
                 name: str,
                 messages: List,
                 release_after: int = None):
        self._trace = Env().get_trace()
        self._name = name
        self._messages = messages
        self._msg_idx = 0
        self._num_rx = 0
        self._done = False
        self._release_after = release_after
        self._event = None
        if self._release_after is not None:
            self._event = threading.Event()
        return

    def __call__(self, *args, **kwargs):
        if self._done:
            assert "Consumer Listener is done: all messages rx'ed"

        msg = kwargs.get('msg', None)
        if msg is None:
            assert ("{} - Expected Message to be passed by name 'msg' to listener, rx'ed {}".format(self._name,
                                                                                                    str(**kwargs)))
        self._trace.log().info("{} - Listener rx'ed message {}".format(self._name, str(msg)))
        self._messages.append(msg)
        self._num_rx = len(self._messages)
        if self._release_after is not None:
            self._trace.log().info(
                "{} of {} messages received".format(str(len(self._messages)), str(self._release_after)))
            if self._num_rx == self._release_after:
                self._done = True
                self._trace.log().info("All messages received, release Event wait")
                self._event.set()
        return

    def wait_until_all_rx(self):
        if self._num_rx is not None and self._event is not None and not self._done:
            self._trace.log().info("Blocking wait for all messages to be rx'ed by Consumer")
            self._event.wait()
            self._trace.log().info("Blocking wait release, all massed rx'ed")
        return


class ProducerTestClient:
    def __init__(self,
                 kps: KPubSub,
                 topic: str,
                 num_msg: int,
                 messages: List,
                 msg_factory: Callable[[], object]):
        """
        On a random timer publish instances of message created with the factory callable.
        :param kps: KPubSub instance to publish via
        :param topic: The Topic string to publish on
        :param num_msg: The number of message to publish before stopping
        :param messages: List to which every sent message is added.
        :param msg_factory: Callable that creates new message objects
        """
        self._trace = Env().get_trace()
        self._num_sent = 0
        self._kps = kps
        self._topic = topic
        self._num_msg = num_msg
        self._messages = messages
        self._msg_factory = msg_factory
        self._runner = threading.Timer(.1, self)
        self._runner.daemon = True
        self._runner.start()
        return

    def __call__(self, *args, **kwargs):
        msg = self._msg_factory()
        self._messages.append(msg)
        self._num_sent += 1
        self._trace.log().info(
            "{} of {} Messages Published:= {}".format(str(self._num_sent), str(self._num_msg), str(msg)))
        self._kps.publish(topic=self._topic, msg=msg)
        if len(self._messages) < self._num_msg:
            self._runner = threading.Timer(np.random.random() * .5, self)
            self._runner.daemon = True
            self._runner.start()
        return

    def __del__(self):
        if self._runner is not None:
            del self._runner


class KPuBsubUtil:
    @staticmethod
    def kpubsub_test(kps: KPubSub,
                     msg_factory: Callable[[], Any],
                     num_msg: int) -> Tuple[List, List]:
        """
        Use message factory to create num_msg messages and send them over Kafka. This verifies the message type
        is correctly set-up to be serialized.

        Utility method that can be called by other object test classes to verify serialisation.
        :param kps: Kafka Pub Sub connection
        :param msg_factory: Callable that creates instances of the messages type under test
        :param num_msg: The number of messages to send.
        """
        topic = UniqueRef().ref
        sent = list()
        rxed = list()
        cl = ConsumerListener('Consumer', messages=rxed, release_after=num_msg)
        kps.subscribe(topic=topic, listener=cl)
        time.sleep(2)
        ptc = ProducerTestClient(kps=kps, topic=topic, num_msg=num_msg, messages=sent, msg_factory=msg_factory)
        cl.wait_until_all_rx()
        del ptc
        del kps
        return sent, rxed


class TestKPubSub(unittest.TestCase):
    # Annotation
    _env: Env
    _trace: Trace
    _run_spec: RunSpec
    _id: int

    # Current Case Id
    _id = 0

    @classmethod
    def setUpClass(cls):
        cls._env = Env()
        cls._trace = cls._env.get_trace()
        cls._run_spec = cls._env.get_context()[EnvBuilder.RunSpecificationContext]
        cls._run_spec.set_spec("kps")
        return

    def setUp(self) -> None:
        self._trace.log().info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestKPubSub._id))
        TestKPubSub._id += 1
        return

    @staticmethod
    def msg_factory() -> object:
        msg = None
        if np.random.random() > 0.5:
            msg = Message1(field1=UniqueRef().ref, field2=np.random.randint(0, 5000))
        else:
            msg = Message2(field3=UniqueRef().ref, field4=np.random.random() * 1000)
        return msg

    def test_kpubsub_single_topic_single_group(self):
        """
        Test random messages being sent over single topic being consumed by a single consumer in a single group
        """
        self._trace.log().info("Test KPubSub Single Topic Single Group")
        expected = list()
        actual = list()
        expected, actual = KPuBsubUtil.kpubsub_test(msg_factory=self.msg_factory,
                                                    num_msg=50)
        self.assertTrue(len(expected) == len(actual))
        for e, a in zip(expected, actual):
            self.assertEqual(e, a)
        return

    def test_kpubsub_single_topic_multi_group(self):
        """
        Create a TestPublisher that pushes various messages types on a timer with a random delay between
        0.0 and 0.5 seconds, where all messages are pushed to the same topic

        """
        kps = KPSUtil(**KPSUtil.args_from_run_spec(self._run_spec)).kps()
        topic = UniqueRef().ref  # Topic not seen by kafka before to keep test clean
        group_1 = UniqueRef().ref
        group_2 = UniqueRef().ref
        messages_sent = list()  # Keep a chronological list of messages sent
        messages_rx1 = list()  # Keep a chronological list of messages received - consumer 1
        messages_rx2 = list()  # Keep a chronological list of messages received - consumer 2

        # Single consumer - should see all messages once in the order sent.
        kps.subscribe(topic=topic, listener=ConsumerListener("Consumer-1", messages=messages_rx1), group=group_1)
        kps.subscribe(topic=topic, listener=ConsumerListener("Consumer-2", messages=messages_rx2), group=group_2)
        time.sleep(2)
        ptc = ProducerTestClient(kps=kps, topic=topic, num_msg=10, messages=messages_sent,
                                 msg_factory=TestKPubSub.msg_factory)
        time.sleep(5)  # Wait for messages to flow.
        # Expect rx = sent, same number, same order - where each consumer gets its own copy
        self.assertEqual(messages_rx1, messages_sent)
        self.assertEqual(messages_rx2, messages_sent)
        del ptc
        del kps
        return

    def test_kpubsub_single_topic_multi_group_multi_consumer(self):
        """
        Create a TestPublisher that pushes various messages types on a timer with a random delay between
        0.0 and 0.5 seconds, where all messages are pushed to the same topic

        """
        kps = KPSUtil(**KPSUtil.args_from_run_spec(self._run_spec)).kps()
        topic = UniqueRef().ref  # Topic not seen by kafka before to keep test clean
        group = UniqueRef().ref
        messages_sent = list()  # Keep a chronological list of messages sent
        messages_rx1 = list()  # Keep a chronological list of messages received - consumer 1
        messages_rx2 = list()  # Keep a chronological list of messages received - consumer 2

        # Single consumer - should see all messages once in the order sent.
        kps.subscribe(topic=topic, listener=ConsumerListener("Consumer-1", messages=messages_rx1), group=group)
        kps.subscribe(topic=topic, listener=ConsumerListener("Consumer-2", messages=messages_rx2), group=group)
        time.sleep(2)
        ptc = ProducerTestClient(kps=kps, topic=topic, num_msg=10, messages=messages_sent,
                                 msg_factory=TestKPubSub.msg_factory)
        time.sleep(10)  # Wait for messages to flow.
        # Expect rx = sent, same number, same order
        # but only one consumer should have got messages
        if len(messages_rx1) == 0:
            self.assertEqual(messages_rx2, messages_sent)
        else:
            self.assertEqual(messages_rx1, messages_sent)
        del ptc
        del kps
        return

    def test_message_map(self):
        message_map = MessageTypeMap(FileStream('message-map.yml'))
        # Verify Header
        self.assertEqual("1.0.0", message_map.version)
        self.assertEqual(datetime.strptime("31 May 2020", "%d %b %Y"), message_map.date)
        self.assertEqual("Map logical message types to message codes", message_map.description)
        # Verify Type to UUID mapping
        self.assertEqual(PBMessage1, message_map.get_protobuf_type_by_uuid("2b352062-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual(PBMessage2, message_map.get_protobuf_type_by_uuid("4395eede-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual(Message1, message_map.get_native_type_by_uuid("2b352062-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual(Message2, message_map.get_native_type_by_uuid("4395eede-a31a-11ea-bb37-0242ac130002"))
        # Verify none when UUID is not in yaml map
        self.assertEqual(None, message_map.get_protobuf_type_by_uuid("7e0014aa-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual(None, message_map.get_native_type_by_uuid("7e0014aa-a31a-11ea-bb37-0242ac130002"))
        # Verify any of the real types map to UUID
        self.assertEqual("2b352062-a31a-11ea-bb37-0242ac130002", message_map.get_uuid_by_type(PBMessage1))
        self.assertEqual("4395eede-a31a-11ea-bb37-0242ac130002", message_map.get_uuid_by_type(PBMessage2))
        self.assertEqual("2b352062-a31a-11ea-bb37-0242ac130002", message_map.get_uuid_by_type(Message1))
        self.assertEqual("4395eede-a31a-11ea-bb37-0242ac130002", message_map.get_uuid_by_type(Message2))
        self.assertEqual(None, message_map.get_uuid_by_type(str))
        # Check partner types
        self.assertEqual(PBMessage1, message_map.get_partner_object_type(Message1))
        self.assertEqual(Message1, message_map.get_partner_object_type(PBMessage1))
        self.assertEqual(PBMessage2, message_map.get_partner_object_type(Message2))
        self.assertEqual(Message2, message_map.get_partner_object_type(PBMessage2))
        self.assertEqual(None, message_map.get_partner_object_type(str))

        return


if __name__ == "__main__":
    unittest.main()
