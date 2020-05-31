from kafka import KafkaProducer
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.lib.kpubsub.pb_notification_pb2 import PBNotification
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap


class Kproducer:
    def __init__(self,
                 server: str,
                 port: str,
                 protoc: ProtoCopy,
                 message_type_map: MessageTypeMap):
        self._server = server
        self._port = port
        self._protoc = protoc
        self._message_type_map = message_type_map
        self.producer = KafkaProducer(bootstrap_servers='{}:{}'.format(self._server, self._port),
                                      value_serializer=None)
        return

    def pub(self,
            topic: str,
            msg) -> None:
        #
        # Encode as bytes and then wrap and send.
        #
        encoded_message = self._protoc.serialize(msg)
        wrapped_message = PBNotification()
        wrapped_message.type_uuid = self._message_type_map.get_uuid_by_type(self._protoc.protobuf_for_object(type(msg)))
        wrapped_message.payload = encoded_message
        _ = self.producer.send(topic, value=wrapped_message.SerializeToString())
        self.producer.flush()
        return
