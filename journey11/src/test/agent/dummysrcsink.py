from typing import List
from pubsub import pub
from journey11.src.interface.capability import Capability
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.ether import Ether
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.lib.uniqueworkref import UniqueWorkRef
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.lib.simplecapability import SimpleCapability
from journey11.src.lib.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.lib.notificationhandler import NotificationHandler


class DummySrcSink(SrcSink):

    def __init__(self,
                 name: str):
        # SrcSink - Standard boot-strap & protected members
        #
        self._name = name
        self._topic = UniqueTopic().topic()
        super().__init__()
        self._capabilities = [SimpleCapability(capability_name='DummySrcSink')]

        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=True)
        self._handler.register_handler(self._srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._srcsink_ping_notification, SrcSinkPingNotification)

        # Public Members just for Unit Test Asserts
        #
        self.pings = list()
        self.ping_notifications = list()

        # Get connected !
        self.setup_subscriptions()
        return

    def __call__(self, notification: Notification):
        """ Handle notification requests
        :param notification: The notification to be passed to the handler
        """
        if isinstance(notification, Notification):
            self._handler.call_handler(notification)
        else:
            raise ValueError("{} un supported notification type {} RX'ed".format(self.name,
                                                                                 type(notification).__name__))
        return

    def setup_subscriptions(self) -> None:
        pub.subscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)
        pub.subscribe(self, self.topic)
        return

    def __del__(self):
        pub.unsubscribesubscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)
        pub.unsubscribe(self, self.topic)
        return

    @property
    def capabilities(self) -> List[Capability]:
        return self._capabilities

    def _srcsink_ping_notification(self, ping_notification: Notification) -> None:
        self.ping_notifications.append(ping_notification)
        return

    def _srcsink_ping(self, ping_request: Notification) -> None:
        self.pings.append(ping_request)
        return

    def send_ping(self,
                  required_capabilities: List[Capability]) -> UniqueWorkRef:
        ping = SimpleSrcSinkPing(sender_srcsink=self, required_capabilities=required_capabilities)
        pub.sendMessage(Ether.ETHER_BACK_PLANE_TOPIC, notification=ping)
        return ping.work_ref

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic
