#
# Kafka PubSub, using Protobuf as the serialisation
#
from typing import Type
import logging
import requests
import io
from journey11.src.lib.loggingsetup import LoggingSetup
from kafka import KafkaProducer
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap


class KPubSub:
    """
    Render file as stream
    """

    class FileStream:
        def __init__(self,
                     filename: str):
            self._filename = filename
            return

        def __call__(self, *args, **kwargs):
            try:
                file_stream = open(self._filename, 'r')
            except Exception as e:
                raise ValueError("File Stream - unable to open {} with error {}".format(self._filename, str(e)))
            return file_stream

    """
    Render URL as stream
    """

    class WebStream:
        def __init__(self,
                     url: str):
            self._url = url
            return

        def __call__(self, *args, **kwargs):
            try:
                url_stream = requests.get(self._url, stream=True)
                if url_stream.encoding is None:
                    url_stream.encoding = 'utf-8'
                res_stream = io.BytesIO(url_stream.content)
                url_stream.close()
            except Exception as e:
                raise ValueError("File Stream - unable read URL {} with error {}".format(self._url, str(e)))
            return res_stream

    def __init__(self,
                 server: str,
                 port: str,
                 yaml_stream):
        """
        :param server: The server on which the Kafka service is running
        :param port: The port on which the Kafka service is listening
        """
        LoggingSetup()
        self._proto_copy = ProtoCopy()
        self._server = server
        self._port = port
        self._message_map = MessageTypeMap(yaml_stream)
        pc = ProtoCopy()
        for native_type, protobuf_type in self._message_map.native_to_protobuf():
            pc.register(native_object_type=native_type, proto_buf_type=protobuf_type)
        return

    def register_message_map(self,
                             object_type: Type,
                             proto_buf_type: Type) -> None:
        """
        Register a mapping between a general 'user' object and the protobuf version.
        :param object_type: The type of the user object
        :param proto_buf_type: The Type of the protobuf equivalent object
        """
        self._proto_copy.register(native_object_type=object_type, proto_buf_type=proto_buf_type)
        return

    def subscribe(self,
                  topic: str,
                  listener) -> None:
        """
        Subscribe to the given topic
        :param topic: The topic to subscribe to
        :param listener: The object that will be called when messages arrive at the topic
        """
        if not hasattr(listener, "__call__"):
            raise ValueError("Listeners must be callable, [{}} is not callable".format(type(listener)))

        if topic not in self._topics:
            self._topics[topic] = list()
        self._topics[topic].append(listener)
        return
