import threading
from typing import Dict
from kafka import KafkaConsumer
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.lib.kpubsub.pb_notification_pb2 import PBNotification
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap


class Kconsumer:
    def __init__(self,
                 listeners: Dict,
                 topic: str,
                 server: str,
                 port: str,
                 protoc: ProtoCopy,
                 message_type_map: MessageTypeMap,
                 group: str = UniqueRef().ref):
        self.consumer = KafkaConsumer(bootstrap_servers='{}:{}'.format(server, port),
                                      group_id=group,
                                      auto_commit=True,
                                      auto_commit_every=10)
        self.consumer.subscribe([topic])
        self._listeners = listeners
        self._protoc = protoc
        self._message_type_map = message_type_map
        self._runner = threading.Timer(.25, self)
        self._runner.start()
        return

    def __call__(self, *args, **kwargs):
        messages = self.consumer.poll(timeout_ms=5, max_records=10)
        for message in messages:
            wrapper_message = PBNotification().ParseFromString(message)
            for listener in self._listeners.values():
                listener_message = self._protoc.deserialize(serialized_src=wrapper_message.payload,
                                                            target_type=self._message_type_map.get_type_by_uuid(
                                                                wrapper_message.type_uuid))
                listener(listener_message)
        return
