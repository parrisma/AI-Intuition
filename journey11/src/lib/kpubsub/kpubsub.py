#
# Kafka PubSub, using Protobuf as the serialisation
#
from typing import Type
import logging
from journey11.src.lib.loggingsetup import LoggingSetup
from kafka import KafkaProducer

from journey11.src.lib.protocopy import ProtoCopy


class KPubSub:

    def __init__(self,
                 server: str,
                 port: str):
        """
        :param server: The server on which the Kafka service is running
        :param port: The port on which the Kafka service is listening
        """
        LoggingSetup()
        self._proto_copy = ProtoCopy()
        self._server = server
        self._port = port
        self._topics = dict()
        return

    def register_message_map(self,
                             object_type: Type,
                             proto_buf_type: Type) -> None:
        """
        Register a mapping between a general 'user' object and the protobuf version.
        :param object_type: The type of the user object
        :param proto_buf_type: The Type of the protobuf equivalent object
        """
        self._proto_copy.register(object_type=object_type, proto_buf_type=proto_buf_type)
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
