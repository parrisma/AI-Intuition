import sys
import unittest
import logging
from datetime import datetime
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap
from journey11.src.lib.kpubsub.kproducer import Kproducer
from journey11.src.lib.kpubsub.kconsumer import Kconsumer
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.test.kpubsub.pb_message1_pb2 import PBMessage1
from journey11.src.test.kpubsub.pb_message2_pb2 import PBMessage2
from journey11.src.test.kpubsub.message2 import Message2
from journey11.src.test.kpubsub.message1 import Message1


class YamlStream:
    def __init__(self,
                 filename: str):
        self._yaml_filename = filename
        return

    def __call__(self, *args, **kwargs):
        return open(self._yaml_filename, 'r')


class TestKPubSub(unittest.TestCase):
    _id = 0

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def setUp(self) -> None:
        logging.info("\n\n- - - - - - C A S E  {} - - - - - -\n\n".format(TestKPubSub._id))
        TestKPubSub._id += 1
        return

    def test_2(self):
        message_map = MessageTypeMap(YamlStream('message-map.yml'))
        pc = ProtoCopy()
        pc.register(object_type=Message1, proto_buf_type=PBMessage1)
        pc.register(object_type=Message2, proto_buf_type=PBMessage2)
        kprod = Kproducer(server="arther", port="9092", protoc=pc, message_type_map=message_map)
        m1 = Message1(field1="Hello World", field2=3142)
        kprod.pub("123", m1)

        return

    def test_message_map_basics(self):
        message_map = MessageTypeMap(YamlStream('message-map.yml'))
        self.assertEqual("1.0.0", message_map.version)
        self.assertEqual(datetime.strptime("31 May 2020", "%d %b %Y"), message_map.date)
        self.assertEqual("Map logical message types to message codes", message_map.description)
        self.assertEqual(PBMessage1, message_map.get_type_by_uuid("2b352062-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual(PBMessage2, message_map.get_type_by_uuid("4395eede-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual(None, message_map.get_type_by_uuid("7e0014aa-a31a-11ea-bb37-0242ac130002"))
        self.assertEqual("2b352062-a31a-11ea-bb37-0242ac130002", message_map.get_uuid_by_type(PBMessage1))
        self.assertEqual("4395eede-a31a-11ea-bb37-0242ac130002", message_map.get_uuid_by_type(PBMessage2))
        self.assertEqual(None, message_map.get_uuid_by_type(str))
        return


if __name__ == "__main__":
    unittest.main()
