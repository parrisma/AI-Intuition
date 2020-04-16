import threading
import logging
from typing import List
from pubsub import pub
from journey11.src.interface.capability import Capability
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.ether import Ether
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotificationfinalise import WorkNotificationFinalise
from journey11.src.interface.worknotificationdo import WorkNotificationDo
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

        self._lock = threading.Lock()
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=True)
        self._handler.register_handler(self._do_srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._do_srcsink_ping_notification, SrcSinkPingNotification)
        self._handler.register_handler(self._do_notification, TaskNotification)
        self._handler.register_handler(self._do_work, WorkNotificationDo)
        self._handler.register_handler(self._do_work_finalise, WorkNotificationFinalise)

        # Public Members just for Unit Test Asserts
        #
        self.pings = list()
        self.ping_notifications = list()
        self.task_notification = list()
        self.work_notification = list()
        self.work_finalise = list()

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
        pub.unsubscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)
        pub.unsubscribe(self, self.topic)
        return

    @property
    def capabilities(self) -> List[Capability]:
        return self._capabilities

    def _do_srcsink_ping_notification(self, ping_notification: Notification) -> None:
        logging.info("{} :: {} RX handled by".format(self.__class__.__name__, self.name, "_srcsink_ping_notification"))
        with self._lock:
            self.ping_notifications.append(ping_notification)
        return

    def _do_srcsink_ping(self, ping_request: Notification) -> None:
        logging.info("{} :: {} RX handled by".format(self.__class__.__name__, self.name, "_srcsink_ping"))
        with self._lock:
            self.pings.append(ping_request)
        return

    def _do_notification(self, task_notification: Notification):
        logging.info("{} :: {} RX handled by".format(self.__class__.__name__, self.name, "_do_notification"))
        with self._lock:
            self.task_notification.append(task_notification)
        return

    def _do_work(self, work_notification: Notification):
        logging.info("{} :: {} RX handled by".format(self.__class__.__name__, self.name, "_do_work"))
        with self._lock:
            self.work_notification.append(work_notification)
        return

    def _do_work_finalise(self, do_work_finalise: Notification):
        logging.info("{} :: {} RX handled by".format(self.__class__.__name__, self.name, "_do_work_finalise"))
        with self._lock:
            self.work_finalise.append(do_work_finalise)
        return

    def send_ping(self,
                  required_capabilities: List[Capability]) -> UniqueWorkRef:
        logging.info("{} :: {} Sent Ping".format(self.__class__.__name__, self.name, "send_ping"))
        ping = SimpleSrcSinkPing(sender_srcsink=self, required_capabilities=required_capabilities)
        pub.sendMessage(Ether.ETHER_BACK_PLANE_TOPIC, notification=ping)
        return ping.work_ref

    @property
    def name(self) -> str:
        return self._name

    @property
    def topic(self) -> str:
        return self._topic
