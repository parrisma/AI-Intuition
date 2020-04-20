import logging
import threading
from typing import List
from pubsub import pub
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.ether import Ether
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.main.simple.simplesrcsinkpingnotification import SimpleSrcSinkNotification
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.main.simple.simplecapability import SimpleCapability


class SimpleEther(Ether):
    ETHER_TOPIC_PREFIX = "ether"
    PING_THRESHOLD = 0.25  # 250ms time after which

    def __init__(self,
                 ether_name: str):
        """
        """
        self._name = ether_name
        self._unique_topic = self._create_topic_and_subscription()
        super().__init__(ether_name)
        self._lock = threading.Lock()
        self._capabilities = [SimpleCapability(str(CapabilityRegister.ETHER))]
        self._ping_factor_threshold = 1.0
        return

    def __del__(self):
        """
        Un subscribe to clean up week refs.
        """
        pub.unsubscribe(self, self._unique_topic)
        pub.unsubscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)
        return

    def _do_srcsink_ping_notification(self,
                                      ping_notification: SrcSinkPingNotification) -> None:
        """
        Handle a ping response from a srcsink
        :param: The srcsink notification
        """
        logging.info("Ether {} RX ping response for {}".format(self.name, ping_notification.src_sink.name))
        if ping_notification.src_sink.topic != self.topic:
            # Don't count ping response from our self.
            for srcsink in ping_notification.responder_address_book:
                self._update_addressbook(sender_srcsink=srcsink)
        return

    def _do_srcsink_ping(self,
                         ping_request: SrcSinkPing) -> None:
        """
        Handle a ping request from a SrcSink
        :param: The srcsink notification
        """
        logging.info("Ether {} RX ping request for {}".format(self.name, ping_request.sender_srcsink.name))
        # Don't count pings from our self.
        if ping_request.sender_srcsink.topic != self.topic:
            # Note the sender is alive
            self._update_addressbook(ping_request.sender_srcsink)
            if Capability.equivalence_factor(ping_request.required_capabilities,
                                             self.capabilities) >= self._ping_factor_threshold:
                pub.sendMessage(topicName=ping_request.sender_srcsink.topic,
                                notification=SimpleSrcSinkNotification(responder_srcsink=self,
                                                                       address_book=[self],
                                                                       sender_workref=ping_request.work_ref))
        return

    @property
    def capabilities(self) -> List[Capability]:
        """
        The capabilities of the Ether
        :return: List of Ether capabilities
        """
        return self._capabilities

    def _create_topic_and_subscription(self) -> str:
        """
        Create the unique topic for the agent that it will listen on for work (task) deliveries that it has
        requested from the task-pool
        """
        topic = UniqueTopic().topic(SimpleEther.ETHER_TOPIC_PREFIX)
        pub.subscribe(self, topic)  # Instance specific
        pub.subscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)  # Back plane discovery topic
        return topic

    @property
    def name(self) -> str:
        """
        The unique name of the SrcSink
        :return: The SrcSink name
        """
        return self._name

    @property
    def topic(self) -> str:
        """
        The unique topic name that SrcSink listens on for activity specific to it.
        :return: The unique SrcSink listen topic name
        """
        return self._unique_topic
