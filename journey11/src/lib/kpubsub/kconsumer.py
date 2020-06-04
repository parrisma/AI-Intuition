import threading
from typing import List
from kafka import KafkaConsumer
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.lib.kpubsub.pb_notification_pb2 import PBNotification
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap


class Kconsumer:
    def __init__(self,
                 listener,
                 topic: str,
                 server: str,
                 port: str,
                 protoc: ProtoCopy,
                 message_type_map: MessageTypeMap,
                 group: str = UniqueRef().ref):
        """
        Boot strap a Kafka listener
        :param listener: The callable object that will be passed the message as key word arg 'msg'
        :param topic:  The Topic to subscribe to
        :param server: The Kafka Server
        :param port: The Kafka Server Port
        :param protoc: The Protoc instance to handle serialise/de-serialise
        :param message_type_map: The mapping between message types and protobuf object handlers
        :param group: The Kafka group to listen as - default is a UUID
        """
        self.consumer = KafkaConsumer(bootstrap_servers='{}:{}'.format(server, port),
                                      group_id=group)
        self.consumer.subscribe([topic])
        self._stop = True
        self._listener = listener
        self._group_id = group
        self._protoc = protoc
        self._message_type_map = message_type_map
        self._runner = self._new_daemon_timer().start()
        self._stop = False
        return

    @property
    def group(self) -> str:
        return self._group_id

    @property
    def topics(self):
        return self.consumer.topics()

    def subscribe(self,
                  topics: List[str],
                  replace: bool = False) -> None:
        """
        Add or replace the given topics to the subscribed topic list for the consumer
        :param topics: The topics to add/replace
        :param replace: If true replace current topics with given topics else add given topics to existing
        :return:
        """
        _topics = list()
        if not replace:
            _topics = list(self.consumer.subscription())
        for t in topics:
            if t not in _topics:
                _topics.append(t)
        self.consumer.subscribe(topics=_topics)
        return

    def _new_daemon_timer(self):
        tmr = threading.Timer(.25, self)
        tmr.daemon = True
        return tmr

    def __call__(self, *args, **kwargs):
        messages_by_partition = self.consumer.poll(timeout_ms=5, max_records=10)
        for topic, messages in messages_by_partition.items():
            for message in messages:
                wrapper_message = PBNotification()
                wrapper_message.ParseFromString(message.value)
                listener_message = self._protoc.deserialize(serialized_src=wrapper_message.payload,
                                                            target_type=self._message_type_map.get_native_type_by_uuid(
                                                                wrapper_message.type_uuid))
                self._listener(msg=listener_message)
        if not self._stop:
            self._runner = self._new_daemon_timer().start()
        return

    def stop(self) -> None:
        self._stop = True
        return

    def __del__(self):
        self.stop()
        runner = getattr(self, "_runner", None)
        if runner is not None:
            del runner
        return
