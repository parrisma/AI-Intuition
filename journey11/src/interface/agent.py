from abc import abstractmethod
from pubsub import pub
from typing import List, List
from journey11.src.interface.notification import Notification
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.interface.worknotificationfinalise import WorkNotificationFinalise
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.ether import Ether
from journey11.src.lib.notificationhandler import NotificationHandler
from journey11.src.lib.purevirtual import purevirtual
from journey11.src.lib.state import State
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.lib.simplecapability import SimpleCapability
from journey11.src.lib.capabilityregister import CapabilityRegister


class Agent(SrcSink):
    WORK_TIMER = float(.25)
    AGENT_TOPIC_PREFIX = "agent"

    def __init__(self,
                 agent_name: str):
        """
        Check this or child class has correctly implemented callable __call__ as needed to handle both the
        PubSub listener events and the work timer events.
        """
        super().__init__()

        self._work_timer = Agent.WORK_TIMER
        self._timer = None
        self._task_consumption_policy = None
        self._handler = NotificationHandler(object_to_be_handler_for=self, throw_unhandled=False)
        self._handler.register_handler(self._do_notification, TaskNotification)
        self._handler.register_handler(self._do_work, WorkNotificationDo)
        self._handler.register_handler(self._do_work_finalise, WorkNotificationFinalise)
        self._handler.register_handler(self._do_srcsink_ping, SrcSinkPing)
        self._handler.register_handler(self._do_srcsink_ping_notification, SrcSinkPingNotification)
        self._handler.register_activity(handler_for_activity=self._work_to_do,
                                        activity_interval=self._work_timer,
                                        activity_name="{}-do_work_activity".format(agent_name))
        self._unique_topic = self._create_topic_and_subscriptions()
        self._capabilities = self._get_capabilities()
        return

    def __del__(self):
        """
        Shut down
        """
        self._handler.activity_state(paused=True)
        pub.unsubscribe(self, self._unique_topic)
        pub.unsubscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)
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
        unique_topic = UniqueTopic().topic(Agent.AGENT_TOPIC_PREFIX)
        pub.subscribe(self, unique_topic)
        pub.subscribe(self, Ether.ETHER_BACK_PLANE_TOPIC)
        return unique_topic

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
                          work_notification: WorkNotificationDo) -> None:
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
    def _work_to_do(self) -> WorkNotificationDo:
        """
        Are there any tasks associated with the Agent that need working on ?
        :return: A WorkNotification event or None if there is no work to do
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
