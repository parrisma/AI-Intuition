import logging
import datetime
import threading
from collections import deque
from typing import Iterable
from pubsub import pub
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinknotification import SrcSinkNotification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.ether import Ether
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.lib.srcsinkwithtimestamp import SrcSinkWithTimeStamp
from journey11.src.lib.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.lib.simplesrcsinkpingnotification import SimpleSrcSinkNotification


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
        self._src_sinks_with_timestamp = dict()
        self._sent = deque(maxlen=1000)
        self._last_pub_time = None
        return

    def _srcsink_notification(self,
                              ping_notification: SrcSinkNotification) -> None:
        """
        Handle a ping response from a player
        :param: The srcsink notification
        """
        logging.info("Ether {} RX ping response for {}".format(self.name, ping_notification.src_sink.name))
        if ping_notification.src_sink.topic != self.topic:
            # Don't count ping response from our self.
            for srcsink in ping_notification.address_book:
                self._update_srcsink(sender_srcsink=srcsink)
        return

    def _srcsink_ping(self,
                      ping_request: SrcSinkPing) -> None:
        """
        Handle a ping response from a player
        :param: The player notification
        """
        logging.info("Ether {} RX ping request for {}".format(self.name, ping_request.sender_srcsink.name))
        if ping_request.sender_srcsink.topic != self.topic:
            # Don't count pings from our self.
            self._update_srcsink(ping_request.sender_srcsink)
            pub.sendMessage(topicName=ping_request.sender_srcsink.topic,
                            notification=SimpleSrcSinkNotification(sender_srcsink=self,
                                                                   address_book=[self]))
        return

    def _do_pub(self) -> None:
        """
        Publish any changes to known players in the ether
        """
        return

    @property
    def _last_pub(self) -> datetime:
        """
        The time at which last pub sent an update
        :return: Time
        """
        if self._last_pub_time is None:
            self._last_pub_time = datetime.datetime(year=1900, month=1, day=1)
        return self._last_pub_time

    @_last_pub.setter
    def _last_pub(self,
                  pub_time: datetime):
        self._last_pub_time = pub_time
        return

    @property
    def srcsinks(self) -> Iterable[SrcSink]:
        """
        The list of players known to the Ether
        :return: Players
        """
        with self._lock:
            srcsinks = list(x.sender_srcsink for x in self._src_sinks_with_timestamp.values())
        return srcsinks

    def _create_topic_and_subscription(self) -> str:
        """
        Create the unique topic for the agent that it will listen on for work (task) deliveries that it has
        requested from the task-pool
        """
        topic = UniqueTopic().topic(SimpleEther.ETHER_TOPIC_PREFIX)
        pub.subscribe(self, topic)  # Instance specific
        pub.subscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)  # Back plane discovery topic
        return topic

    def _update_srcsink(self,
                        sender_srcsink: SrcSink) -> None:
        """
        Update the given src_sink in the collection of registered players. If src_sink is not in the collection
        add it with a current time stamp.
        :param srcsink: The src_sink to update / add.
        """
        sender_name = sender_srcsink.name
        with self._lock:
            if sender_name not in self._src_sinks_with_timestamp:
                self._src_sinks_with_timestamp[sender_name] = SrcSinkWithTimeStamp(sender_srcsink=sender_srcsink,
                                                                                   time_stamp=datetime.datetime.now())
            else:
                self._src_sinks_with_timestamp[sender_name].time_stamp = datetime.datetime.now()
        return

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
