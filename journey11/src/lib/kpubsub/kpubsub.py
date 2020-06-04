#
# Kafka PubSub, using Protobuf as the serialisation
#
from typing import Type
import logging
import requests
import io
import re
from journey11.src.lib.protocopy import ProtoCopy
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap
from journey11.src.lib.kpubsub.kconsumer import Kconsumer
from journey11.src.lib.kpubsub.kproducer import Kproducer
from journey11.src.lib.uniqueref import UniqueRef


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
        self._server = server
        self._port = port
        logging.info("Kafka-PubSub established for {}:{}".format(self._server, self._port))

        self._message_map = MessageTypeMap(yaml_stream)
        self._proto_copy = ProtoCopy()
        for native_type, protobuf_type in self._message_map.native_to_protobuf():
            self._proto_copy.register(native_object_type=native_type, proto_buf_type=protobuf_type)
            logging.info(
                "Kafka PubSub - created message type map entry native:{} <-> protobuf:{}".format(str(native_type),
                                                                                                 str(protobuf_type)))
        self._consumers = dict()
        self._producer = self._init_producer()
        return

    def _init_producer(self) -> Kproducer:
        """
        Create the Kafka Producer
        :return: The Kafka Producer
        """
        return Kproducer(server=self._server,
                         port=self._port,
                         protoc=self._proto_copy,
                         message_type_map=self._message_map)

    def _subscribe(self,
                   listener,
                   topic: str,
                   group: str = None) -> Kconsumer:
        """
        Create default consumer registered on default group
        :return: Kafka Consumer resgistered to default group.
        """
        self._exception_if_not_callable_or_hashable(listener)

        group = self._clean_and_default_group(group=group)

        key = self._group_listener_key(group=group, listener=listener)

        if key not in self._consumers:
            # A new listener and/or group - so create new consumer
            kcons = Kconsumer(listener=listener,
                              topic=topic,
                              server=self._server,
                              port=self._port,
                              protoc=self._proto_copy,
                              group=group,
                              message_type_map=self._message_map)
            self._consumers[key] = kcons
        else:
            # An existing listener & group - so just subscribe to new topic
            kcons = self._consumers[key]
            kcons.subscribe(topics=[topic])

        return kcons

    def register_message_map(self,
                             native_type: Type,
                             protobuf_type: Type) -> None:
        """
        Register a mapping between a general 'user' object and the protobuf version.
        :param native_type: The type of the user object
        :param protobuf_type: The Type of the protobuf equivalent object
        """
        self._proto_copy.register(native_object_type=native_type, proto_buf_type=protobuf_type)
        logging.info(
            "Kafka PubSub - created message type map entry native:{} <-> protobuf:{}".format(str(native_type),
                                                                                             str(protobuf_type)))
        return

    def subscribe(self,
                  topic: str,
                  listener,
                  group: str = None) -> None:
        """
        Subscribe to the given topic
        :param topic: The topic to subscribe to
        :param group: Optional Kafka group, if not supplied a default unique group is used.
        :param listener: The object that will be called when messages arrive at the topic
        """
        _ = self._subscribe(topic=topic, group=group, listener=listener)
        return

    def publish(self,
                topic: str,
                msg) -> None:
        """
        Publish the given message to the given topic
        :param topic: The topic to publish to
        :param msg: The message object to publish
                    Note: message type must be registered in the message-map.yaml
        """
        self._producer.pub(topic=topic, msg=msg)
        return

    def __del__(self):
        """
        Clean up all running consumers
        """
        for kcons in self._consumers:
            del kcons
        return

    @staticmethod
    def _exception_if_not_callable_or_hashable(listener) -> None:
        """
        Listen objects must be callable and hashable. This method will raise an exception if the given
        object is either not callable or hashable
        :param listener: The object to be checked.
        """
        if listener is None or not hasattr(listener, "__call__"):
            raise ValueError("Listeners must be callable, [{}} is not callable".format(type(listener)))

        if not hasattr(listener, "__hash__") or not hasattr(listener, "__eq__"):
            raise ValueError(
                "Listeners must be hashable, [{}} is missing __eq__ and/or __hash__".format(type(listener)))
        return

    @staticmethod
    def _clean_and_default_group(group: str) -> str:
        """
        If group is None assign it a unique default value or remove trailing whitespace
        :param group: The group name to be cleaned or defaulted
        :return: The cleaned or defaulted group name
        """
        if group is None:
            group = ""
        group = re.sub(pattern=r"^\s+|\s+$", repl="", string=group)
        if len(group) == 0:
            group = UniqueRef().ref
        return group

    @staticmethod
    def _group_listener_key(group: str,
                            listener) -> str:
        """
        Create an immutable key from the given group + listener. We only now that the listener is
        hashable and the the hash is immutable for the life of the object so we combine the group
        and the string equiv of the listener hash.
        :param group: The group name to build the key from
        :param listener: The listener object to build the key from
        :return: The key as a string
        """
        return "{}-{}".format(group, str(listener.__hash__()))
