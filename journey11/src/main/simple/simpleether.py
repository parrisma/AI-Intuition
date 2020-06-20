import logging
import threading
from typing import List
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.ether import Ether
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.main.simple.simplekps import SimpleKps
from journey11.src.main.simple.simplesrcsinkpingnotification import SimpleSrcSinkPingNotification


class SimpleEther(Ether):
    ETHER_TOPIC_PREFIX = "ether"
    PING_THRESHOLD = 0.25  # 250ms time after which ?

    def __init__(self,
                 ether_name: str):
        """
        """
        self._name = ether_name
        super().__init__(ether_name)
        self._lock = threading.Lock()
        self._capabilities = [SimpleCapability(str(CapabilityRegister.ETHER))]
        self._ping_factor_threshold = 1.0
        self._kps = SimpleKps()
        self._unique_topic = self._create_topic_and_subscription()  # must follow _kps set up
        return

    def _do_srcsink_ping_notification(self,
                                      ping_notification: SrcSinkPingNotification) -> None:
        """
        Handle a ping response from a srcsink
        :param: The srcsink ping notification
        """
        Trace.log().info(
            "Ether {}-{} RX ping response for {}".format(self.name, self.topic, ping_notification.src_sink.name))
        # Only count ping response of not from our self.
        if ping_notification.src_sink.topic != self.topic:
            for srcs_ink_proxy in ping_notification.responder_address_book:
                self._update_address_book()
        return

    def _do_srcsink_ping(self,
                         ping_request: SrcSinkPing) -> None:
        """
        Handle a ping request from a SrcSink
        :param: The srcsink notification
        """
        Trace.log().info(
            "Ether {}-{} RX ping request for {}".format(self.name, self.topic, ping_request.sender_srcsinkproxy.name))
        # Don't count pings from our self.
        if ping_request.sender_srcsinkproxy.topic != self.topic:
            # Note the sender is alive
            self._update_address_book(ping_request.sender_srcsinkproxy)
            addrs = self._get_addresses_with_capabilities(ping_request.required_capabilities)
            self._kps.connection.publish(topic=ping_request.sender_srcsinkproxy.topic,
                                         msg=SimpleSrcSinkPingNotification(work_ref=ping_request.work_ref,
                                                                           responder_srcsink=self,
                                                                           address_book=addrs))
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
        self._kps.connection.subscribe(topic=topic, listener=self)
        self._kps.connection.subscribe(topic=Ether.ETHER_BACK_PLANE_TOPIC, listener=self)
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

    def _do_pub(self) -> None:
        """
        Not implemented
        :return: None
        """
        # TODO: this will be target of Ether Activity to ping and refresh expired addresses
        pass

    def __str__(self) -> str:
        return "Ether {} on Topic {} with Capabilities {}".format(self._name, self._unique_topic, self._capabilities)

    def __repr__(self) -> str:
        return self.__str__()
