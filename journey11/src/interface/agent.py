import threading
from copy import deepcopy
from abc import abstractmethod
from pubsub import pub
from typing import List
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.interface.worknotificationfinalise import WorkNotificationFinalise
from journey11.src.interface.worknotificationinitiate import WorkNotificationInitiate
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.state import State
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.main.simple.simplecapability import SimpleCapability
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.lib.addressbook import AddressBook


class Agent(SrcSink):
    WORK_TIMER = float(.25)
    WORK_TIMER_MAX = float(30)
    PRS_TIMER = float(.25)
    PRD_TIMER_MAX = float(60)
    WORK_INIT_TIMER = float(.25)
    WORK_INIT_TIMER_MAX = float(180)
    AGENT_TOPIC_PREFIX = "agent"

    def __init__(self,
                 agent_name: str):
        """
        Register all notification handlers & activities.
        """
        self._address_book = AddressBook()
        self._lock = threading.RLock()
        self._subscribed_topics = list()

        super().__init__()

        self._work_timer = Agent.WORK_TIMER
        self._timer = None
        self._task_consumption_policy = None
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=False)
        self._handler.register_handler(self._do_notification, TaskNotification)
        self._handler.register_handler(self._do_work, WorkNotificationDo)
        self._handler.register_handler(self._do_work_finalise, WorkNotificationFinalise)
        self._handler.register_handler(self._do_work_initiate, WorkNotificationInitiate)
        self._handler.register_handler(self._do_srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._do_srcsink_ping_notification, SrcSinkPingNotification)
        self._handler.register_activity(handler_for_activity=self._activity_check_work_to_do,
                                        activity_interval=self._work_timer,
                                        activity_name="{}-activity-work-to-do".format(agent_name))
        self._handler.register_activity(handler_for_activity=self._activity_manage_presence,
                                        activity_interval=Agent.PRS_TIMER,
                                        activity_name="{}-activity-manage-presence".format(agent_name))
        self._handler.register_activity(handler_for_activity=self._activity_initiate_work,
                                        activity_interval=Agent.WORK_INIT_TIMER,
                                        activity_name="{}-activity-work-init".format(agent_name))
        self._unique_topic = self._create_topic_and_subscriptions()
        self._capabilities = self._get_capabilities()
        return

    def __del__(self):
        """
        Shut down
        """
        self._handler.activity_state(paused=True)
        with self._lock:
            sub_list = deepcopy(self._subscribed_topics)
        for topic in sub_list:
            pub.unsubscribe(self, topic)
        return

    def __call__(self, notification: Notification):
        """ Handle notification requests
        :param notification: The notification to be passed to the handler
        """
        if isinstance(notification, Notification):
            self._handler.call_handler(notification)
        else:
            raise ValueError("{} is an un supported notification type for Agent}".format(type(notification).__name__))
        return

    def _create_topic_and_subscriptions(self) -> str:
        """
        Create the unique topic for the agent that it will listen on for work (task) deliveries that it has
        requested from the task-pool
        """
        topics = list()
        unique_topic = UniqueTopic().topic(Agent.AGENT_TOPIC_PREFIX)
        topics.append(unique_topic)
        for topic in self._work_topics():
            topics.append(topic)
        self.add_subscription_topics(topics=topics)
        for topic in topics:  # do potentially high latency subscriptions outside of the lock.
            pub.subscribe(self, topic)
        return unique_topic

    def add_subscription_topics(self,
                                topics: List[str]) -> None:
        """
        Add the given list of topics to the list of topics agent is subscribed to
        """
        with self._lock:
            for topic in topics:
                if topic not in self._subscribed_topics:
                    self._subscribed_topics.append(topic)
        return

    @staticmethod
    def _get_capabilities() -> List[Capability]:
        """
        The capabilities of this Agent
        :return: List of Capabilities
        """
        return [SimpleCapability(capability_name=str(CapabilityRegister.AGENT))]

    @abstractmethod
    @purevirtual
    def _do_notification(self,
                         task_notification: TaskNotification):
        """
        callback to Notify agent of a task that needs attention. The agent can optionally grab the task from the
        task pool and work on it or ignore it.
        :param task_notification: The notification event for task requiring attention
        """
        pass

    @abstractmethod
    @purevirtual
    def _do_work(self,
                 work_notification: WorkNotificationDo) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
        pass

    @abstractmethod
    @purevirtual
    def _do_work_initiate(self,
                          work_notification: WorkNotificationInitiate) -> None:
        """
        Handle the initiation the given work item from this agent
        """
        pass

    @abstractmethod
    @purevirtual
    def _do_work_finalise(self,
                          work_notification_finalise: WorkNotificationFinalise) -> None:
        """
        Take receipt of the given completed work item that was initiated from this agent and do any
        final processing.
        """
        pass

    @abstractmethod
    @purevirtual
    def work_initiate(self,
                      work_notification: WorkNotificationDo) -> None:
        """
        Initiate the given work item with the agent as the owner of the work.
        """
        pass

    @abstractmethod
    @purevirtual
    def _activity_check_work_to_do(self,
                                   current_activity_interval: float) -> float:
        """
        Are there any tasks associated with the Agent that need working on ? of so schedule them by calling work
        execute handler.
        :param current_activity_interval: The current delay in seconds before activity is re-triggered.
        :return: The new delay in seconds before the activity is re-triggered.
        """

        pass

    @purevirtual
    @abstractmethod
    def _activity_manage_presence(self,
                                  current_activity_interval: float) -> float:
        """
        Ensure that we are known on the ether & our address book has the name of at least one local pool in it.
        :param current_activity_interval: The current delay in seconds before activity is re-triggered.
        :return: The new delay in seconds before the activity is re-triggered.
        """
        pass

    @purevirtual
    @abstractmethod
    def _activity_initiate_work(self,
                                current_activity_interval: float) -> float:
        """
        If the agent is a source (origin) of work then this activity will create and inject the new tasks. Zero
        or more tasks may be created depending on the specific task creation policy.
        :param current_activity_interval: The current delay in seconds before activity is re-triggered.
        :return: The new delay in seconds before the activity is re-triggered.
        """
        pass

    @purevirtual
    @abstractmethod
    def _work_topics(self) -> List[str]:
        """
        The list of topics to subscribe to based on the Work Topics (status transitions) supported by the
        agent.
        """
        pass

    @property
    def task_consumption_policy(self) -> TaskConsumptionPolicy:
        """
        Get the policy that the agent uses to decide to process (or not) the task based on tasks meta data
        :return: The consumption policy
        """
        return self._task_consumption_policy

    @task_consumption_policy.setter
    def task_consumption_policy(self,
                                p: TaskConsumptionPolicy) -> None:
        """
        Set the policy that the agent uses to decide to process (or not) the task based on tasks meta data
        """
        self._task_consumption_policy = p

    @abstractmethod
    @purevirtual
    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        pass

    # ----- P R O P E R T I E S -----

    @property
    @abstractmethod
    @purevirtual
    def name(self) -> str:
        """
        The unique name of the Agent
        :return: The Agent name
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        pass

    @abstractmethod
    @purevirtual
    @property
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        pass

    @abstractmethod
    @purevirtual
    @property
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        pass

    @property
    def work_interval(self) -> float:
        """
        The wait period between doing work.
        :return: Wait interval between work timer events in seconds
        """
        return self._work_timer

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
