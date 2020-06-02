import socket
import numpy as np
import unittest
import logging
import threading
import time
from typing import List
from datetime import datetime
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap
from journey11.src.lib.kpubsub.kpubsub import KPubSub
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.test.kpubsub.pb_message1_pb2 import PBMessage1
from journey11.src.test.kpubsub.pb_message2_pb2 import PBMessage2
from journey11.src.test.kpubsub.message2 import Message2
from journey11.src.test.kpubsub.message1 import Message1


class ConsumerListener:
    def __init__(self,
                 messages: List):
        self._messages = messages
        self._msg_idx = 0
        return

    def __call__(self, *args, **kwargs):
        msg = kwargs.get('msg', None)
        if msg is None:
            assert ("Expected Message to be passed by name 'msg' to listener, rx'ed {}".format(str(**kwargs)))
        logging.info("Listener rx'ed message {}".format(str(msg)))
        if msg != self._messages[self._msg_idx]:
            assert ("Messages not same as message sent {} != {} @ idx {}".format(str(msg),
                                                                                 str(self._messages[self._msg_idx]),
                                                                                 str(self._msg_idx)))
        return


class ProducerTestClient:
    def __init__(self,
                 kps: KPubSub,
                 topic: str,
                 num_msg: int,
                 messages: List):
        self._kps = kps
        self._topic = topic
        self._num_msg = num_msg
        self._messages = messages
        self._runner = threading.Timer(.1, self)
        self._runner.daemon = True
        self._runner.start()
        return

    def __call__(self, *args, **kwargs):
        if np.random.random() > 0.5:
            msg = Message1(field1=UniqueRef().ref, field2=np.random.randint(0, 5000))
        else:
            msg = Message2(field3=UniqueRef().ref, field4=np.random.random() * 1000)
        self._messages.append(msg)
        logging.info("Published message {}".format(str(msg)))
        self._kps.publish(topic=self._topic, msg=msg)
        if len(self._messages) < self._num_msg:
            self._runner = threading.Timer(np.random.random() * .5, self)
            self._runner.daemon = True
            self._runner.start()
        return

    def __del__(self):
        if self._runner is not None:
            del self._runner


class TestKPubSub(unittest.TestCase):
    _id = 0

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestKPubSub._id))
        TestKPubSub._id += 1
        return

    def test_kpubsub(self):
        """
        Create a TestPublisher that pushes various messages types on a timer with a random delay between
        0.0 and 0.5 seconds. Record all messages sent in a list.

        Create a TesConsumer that connects to the same topic make a record of all messages rx'ed.

        Check messages sent are same as messages rx'ed and in the same order. Order should be preserved as the
        consumer is in unique kafka-group with no other consumers in that group.
        """
        # We expect a Kafka server running the same machine as this test. This can be run up with the Swarm service
        # or stand along container script that is also part of this project.
        hostname = socket.gethostbyname(socket.gethostname())
        port_id = '9092'
        topic = UniqueRef().ref
        kps = KPubSub(server=hostname,
                      port=port_id,
                      yaml_stream=KPubSub.WebStream(
                          'https://raw.githubusercontent.com/parrisma/AI-Intuition/master/journey11/src/test/kpubsub/message-map.yml'))
        messages_sent = list()
        kps.subscribe(topic=topic, listener=ConsumerListener(messages=messages_sent))
        ptc = ProducerTestClient(kps=kps, topic=topic, num_msg=10, messages=messages_sent)
        time.sleep(10)
        print(messages_sent)
        del ptc
        del kps
        return

    def test_message_map(self):
        message_map = MessageTypeMap(KPubSub.FileStream('message-map.yml'))
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
