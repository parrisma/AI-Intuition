from abc import abstractmethod
from typing import List
import threading
from pubsub import pub
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.workrequest import WorkRequest
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.interface.worknotificationfinalise import WorkNotificationFinalise
from journey11.src.interface.notification import Notification
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.state import State
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.lib.addressbook import AddressBook


class TaskPool(SrcSink):
    PUB_TIMER = float(.25)
    PUB_TIMER_MAX = float(30)
    PRS_TIMER = float(.25)
    PRS_TIMER_MAX = float(30)
    POOL_TOPIC_PREFIX = "TaskPool"

    def __init__(self,
                 pool_name: str):
        """
        Check this or child class has correctly implemented callable __call__ as needed to handle both the
        PubSub listener events and the work timer events.
        """
        self._address_book = AddressBook()
        super().__init__()
        self._call_lock = threading.Lock()
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=False)
        self._handler.register_handler(self._get_task, WorkRequest)
        self._handler.register_handler(self._put_task, WorkNotificationDo)
        self._handler.register_handler(self._do_srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._do_srcsink_ping_notification, SrcSinkPingNotification)
        self._handler.register_handler(self._do_work_finalise, WorkNotificationFinalise)
        self._handler.register_activity(handler_for_activity=self._do_pub,
                                        activity_interval=TaskPool.PUB_TIMER,
                                        activity_name="{}-do_pub_activity".format(pool_name))
        self._handler.register_activity(handler_for_activity=self._do_manage_presence,
                                        activity_interval=TaskPool.PRS_TIMER,
                                        activity_name="{}-do_manage_presence".format(pool_name))
        self._capabilities = self._get_capabilities()
        self._unique_topic = self._create_topic_and_subscription()
        return

    def __del__(self):
        """
        Clean up
        """
        self._handler.activity_state(paused=True)
        pub.unsubscribe(self, self._unique_topic)
        return

    def __call__(self, notification: Notification):
        """ Handle notification requests
        :param notification: The notification to be passed to the handler
        """
        if isinstance(notification, Notification):
            self._handler.call_handler(notification)
        else:
            raise ValueError("{} un supported notification type for Task Pool".format(type(notification).__name__))
        return

    def _create_topic_and_subscription(self) -> str:
        """
        Create the unique topic for the agent that it will listen on for work (task) deliveries that it has
        requested from the task-pool
        """
        unique_topic = UniqueTopic().topic(TaskPool.POOL_TOPIC_PREFIX)
        pub.subscribe(self, unique_topic)
        return unique_topic

    @staticmethod
    def _get_capabilities() -> List[Capability]:
        """
        The capabilities of this Agent
        :return: List of Capabilities
        """
        return [SimpleCapability(capability_name=str(CapabilityRegister.POOL))]

    @purevirtual
    @abstractmethod
    def _put_task(self,
                  work_initiate: WorkNotificationDo) -> None:
        """
        Add a task to the task pool which will cause it to be advertised via the relevant topic unless the task
        is in it's terminal state.
        :param work_initiate: Details of the task being injected.
        """
        pass

    @purevirtual
    @abstractmethod
    def _get_task(self,
                  work_request: WorkRequest) -> None:
        """
        Send the requested task to the consumer if the task has not already been sent to a consumer
        :param work_request: The details of the task and the consumer
        """
        pass

    @purevirtual
    @abstractmethod
    def _do_pub(self,
                current_interval: float) -> float:
        """
        Check for any pending tasks and advertise or re-advertise them on the relevant topic
        :param current_interval: The current activity interval
        :return: The optionally revised interval before the action is invoked again
        """
        pass

    @purevirtual
    @abstractmethod
    def _do_manage_presence(self,
                            current_interval: float) -> float:
        """
        Ensure that we are known on the ether.
        :param current_interval: The current activity interval
        :return: The optionally revised interval before the action is invoked again
        """
        pass

    @purevirtual
    @abstractmethod
    def _do_work_finalise(self,
                          work_notification_final: WorkNotificationFinalise) -> None:
        """
        Handle the event where a task is in terminal state with no work to do. Default is to notify the
        originator of the task that their work is done by forwarding the finalise notification.
        """
        pass

    @classmethod
    def topic_for_capability(cls,
                             state: State) -> str:
        """
        The topic string on which tasks needing work in that state are published on
        :param state: The state for which the topic is required
        :return: The topic string for the given state
        """
        # TODO https://github.com/parrisma/AI-Intuition/issues/1
        return "topic-{}".format(str(state.id()))

    @property
    @abstractmethod
    @purevirtual
    def name(self) -> str:
        """
        The name of the task pool
        :return: The name of the task pool as string
        """
        pass

    @property
    def capabilities(self) -> List[Capability]:
        """
        The collection of capabilities of the SrcSink
        :return: The collection of capabilities
        """
        return self._capabilities

    def get_addressbook(self) -> List[SrcSink]:
        """
        The list of srcsinks known to the Ether
        :return: srcsinks
        """
        return self._address_book.get()

    def _update_addressbook(self,
                            srcsink: SrcSink) -> None:
        """
        Update the given src_sink in the collection of registered srcsinks. If src_sink is not in the collection
        add it with a current time stamp.
        :param srcsink: The src_sink to update / add.
        """
        self._address_book.update(srcsink)
        return

    def _get_recent_ether_address(self) -> SrcSink:
        """
        Get a recent Ether address from the AddressBook. If there is no recent Ether then return None
        :return: Ether SrcSink or None
        """
        ss = self._address_book.get_with_capabilities(
            required_capabilities=[SimpleCapability(str(CapabilityRegister.ETHER))],
            max_age_in_seconds=60,
            n=1)
        if ss is not None:
            ss = ss[0]
        return ss
