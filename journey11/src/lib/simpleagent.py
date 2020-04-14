import logging
import threading
from queue import Queue
from pubsub import pub
from typing import Type, Dict, List
from journey11.src.interface.agent import Agent
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.interface.worknotificationfinalise import WorkNotificationFinalise
from journey11.src.interface.capability import Capability
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.lib.simplesrcsinkpingnotification import SimpleSrcSinkNotification
from journey11.src.lib.state import State
from journey11.src.lib.simpleworkrequest import SimpleWorkRequest
from journey11.src.lib.simplecapability import SimpleCapability
from journey11.src.lib.capabilityregister import CapabilityRegister


class SimpleAgent(Agent):
    FAIL_RATE = float(0)

    def __init__(self,
                 agent_name: str,
                 start_state: State,
                 end_state: State,
                 capacity: int,
                 task_consumption_policy: TaskConsumptionPolicy,
                 trace: bool = False):
        """
        """
        self._agent_name = agent_name
        self._start_state = start_state
        self._end_state = end_state

        super().__init__(agent_name)

        self._fail_rate = SimpleAgent.FAIL_RATE
        self._capacity = capacity

        self._work_lock = threading.Lock()
        self._work_pending = Queue()
        self._work_in_progress = Queue()
        self._work_done = Queue()

        self._num_notification = 0
        self._num_work = 0

        self._task_consumption_policy = task_consumption_policy

        self._trace = trace
        self._trace_log = dict()

        self._ping_factor_threshold = float(1)

        return

    def __del__(self):
        super().__del__()
        return

    @property
    def name(self) -> str:
        """
        The unique name of the Agent
        :return: The Agent name
        """
        return self._agent_name

    @property
    def topic(self) -> str:
        """
        The unique topic name that agent listens on for activity specific to it.
        :return: The unique agent listen topic name
        """
        return self._unique_topic

    def _do_notification(self,
                         task_notification: TaskNotification):
        """
        callback to Notify agent of a task that needs attention. The agent can request the task be sent to it for
        processing but there is no guarantee as another agent may have already requested the task.
        :param task_notification: The notification event for task requiring attention
        """
        self._trace_log_update("_do_notification", type(task_notification), task_notification.work_ref.id)
        logging.info("{} do_notification for work ref {}".format(self._agent_name, task_notification.work_ref.id))
        self._num_notification += 1
        if self._task_consumption_policy.process_task(task_notification.task_meta):
            if task_notification.originator is not None:
                work_request = SimpleWorkRequest(task_notification.work_ref, self)
                pub.sendMessage(topicName=task_notification.originator.topic, notification=work_request)
                logging.info("{} sent request for work ref {} OK from pool {}".format(self._agent_name,
                                                                                      task_notification.work_ref.id,
                                                                                      task_notification.originator.name))
            else:
                logging.error("{} notification IGNORED as no originator address given for work ref {}".format(
                    self._agent_name,
                    task_notification.work_ref.id))
        else:
            self._num_notification -= 1
            logging.info("{} Rx TaskNotification Ignored by Consumption Policy{}".format(self.name,
                                                                                         task_notification.work_ref.id))
        return

    def _do_work(self,
                 work_notification: WorkNotificationDo) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
        self._trace_log_update("_do_work", type(work_notification), work_notification.work_ref.id)
        self._num_work += 1
        if work_notification.task.work_in_state_remaining > 0:
            logging.info("{} do_work for work_ref {}".format(self._agent_name, work_notification.work_ref.id))
            if work_notification.task.do_work(self.capacity) > 0:
                logging.info("{} do_work for task id {} - task rescheduled with {} work remaining in state {}".format(
                    self._agent_name, work_notification.task.id,
                    work_notification.task.work_in_state_remaining,
                    work_notification.task.state))
                self._add_work_item_to_queue(work_notification)
        else:
            logging.info("{} do_work nothing left to do for task {} in state {}".format(self._agent_name,
                                                                                        work_notification.task.id,
                                                                                        work_notification.task.state))

        # If work remaining is zero, need to transition to next state and post the task back to the
        # originator
        #
        if work_notification.task.work_in_state_remaining == 0:
            work_notification.task.state = self.to_state
            pub.sendMessage(topicName=work_notification.originator.topic, notification=work_notification)
            logging.info("{} send task {} to pool {} in state {}".format(self._agent_name,
                                                                         work_notification.task.id,
                                                                         work_notification.originator.name,
                                                                         work_notification.task.state))
        return

    def _add_work_item_to_queue(self,
                                work_notification: WorkNotificationDo) -> None:
        self._work_in_progress.put(work_notification)
        return

    def _do_work_initiate(self,
                          work_notification: WorkNotificationDo) -> None:
        """
        Handle the initiation the given work item from this agent
        """
        with self._work_lock:
            self._work_pending.put(work_notification)
        return

    def _do_work_finalise(self,
                          work_notification_final: WorkNotificationFinalise) -> None:
        """
        Take receipt of the given completed work item that was initiated from this agent and do any
        final processing.
        """
        logging.info("{} Rx Finalised task {} from source {} in state {}".format(self._agent_name,
                                                                                 work_notification_final.task.id,
                                                                                 work_notification_final.originator.name,
                                                                                 work_notification_final.task.state))
        return

    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        return

    def _work_to_do(self) -> None:
        """
        Are there any tasks associated with the Agent that need working on ? if so invoke the do_work method for
        every task that needs work.
        """
        if not self._work_in_progress.empty():
            wtd = self._work_in_progress.get()
            logging.info("{} work_to_do for task ref {}".format(self._agent_name, wtd.work_ref.id))
            self._do_work(wtd)
        else:
            logging.info("{} work_to_do - nothing to do".format(self._agent_name))
        return

    def work_initiate(self, work_notification: WorkNotificationDo) -> None:
        """
        Initiate the given work item with the agent as the owner of the work.
        """
        raise NotImplementedError("work_initiate missing")

    def _trace_log_update(self,
                          func: str,
                          action_type: Type,
                          work_ref_id) -> None:
        """ Keep a record of all the notification events for this agent
        For unit testing only
        :param func: The notification function called
        :param action_type: The type of the action passed to the notification function
        :param work_ref_id: the work ref id of the notification
        """
        if self._trace:
            tlid = self.trace_log_id(func, action_type, work_ref_id)
            if tlid not in self._trace_log:
                self._trace_log[tlid] = 1
            else:
                cnt = self._trace_log[tlid]
                self._trace_log[tlid] = cnt + 1
        return

    @staticmethod
    def trace_log_id(func: str,
                     action_type: Type,
                     work_ref_id) -> str:
        """ Create a key to hold a trace log record against

        :param func: The notification function called
        :param action_type: The type of the action passed to the notification function
        :param work_ref_id: the work ref id of the notification
        :return: The key
        """
        return "{}{}{}".format(func, action_type.__name__, work_ref_id)

    # ----- P R O P E R T I E S -----

    @property
    def trace_log(self) -> Dict:
        """The trace log where agent notifications are tracked
        For test validation only
        :return: Trace Log Dictionary
        """
        return self._trace_log

    @property
    def capacity(self) -> int:
        """
        The current work capacity of the actor.
        :return: Current work capacity as int
        """
        return self._capacity

    @property
    def from_state(self) -> State:
        """
        The state the actor expects to receive tasks in
        :return: from state
        """
        return self._start_state

    @property
    def to_state(self) -> State:
        """
        The state the actor will process tasks into
        :return: to state
        """
        return self._end_state

    @property
    def failure_rate(self) -> float:
        """
        The rate at which completed tasks fail.
        :return: Failure state of the actor
        """
        return self._fail_rate

    @failure_rate.setter
    def failure_rate(self,
                     r: float) -> None:
        """
        The rate at which completed tasks fail.
        :param r: the failure state of the actor
        """
        if r < 0.0 or r > 1.0:
            raise ValueError("Failure rate for Agent must be between 0.0 and 1.0")
        self._fail_rate = r

    def __str__(self):
        s = "Agent [{}] from state {} to state {}".format(self._agent_name,
                                                          str(self._start_state),
                                                          str(self._end_state)
                                                          )
        return s

    @property
    def num_notification(self) -> int:
        """
        How many task notifications did the agent get
        :return: num notifications
        """
        return self._num_notification

    @property
    def num_work(self) -> int:
        """
        How many tasks did the agent work on
        :return: num tasks worked on
        """
        return self._num_work

    @property
    def capabilities(self) -> List[Capability]:
        """
        The capabilities of the Ether
        :return: List of Ether capabilities
        """
        return self._capabilities

    def _srcsink_ping_notification(self,
                                   ping_notification: SrcSinkPingNotification) -> None:
        """
        Handle a ping response from a srcsink
        :param: The srcsink notification
        """
        logging.info("Ether {} RX ping response for {}".format(self.name, ping_notification.src_sink.name))
        if ping_notification.src_sink.topic != self.topic:
            # Don't count ping response from our self.
            for srcsink in ping_notification.responder_address_book:
                self._update_srcsink_addressbook(sender_srcsink=srcsink)
        return

    def _srcsink_ping(self,
                      ping_request: SrcSinkPing) -> None:
        """
        Handle a ping response from a srcsink
        :param: The srcsink notification
        """
        logging.info("Ether {} RX ping request for {}".format(self.name, ping_request.sender_srcsink.name))
        # Don't count pings from our self.
        if ping_request.sender_srcsink.topic != self.topic:
            # Note the sender is alive
            self._update_srcsink_addressbook(ping_request.sender_srcsink)
            if Capability.equivalence_factor(ping_request.required_capabilities,
                                             self.capabilities) >= self._ping_factor_threshold:
                pub.sendMessage(topicName=ping_request.sender_srcsink.topic,
                                notification=SimpleSrcSinkNotification(responder_srcsink=self,
                                                                       address_book=[self],
                                                                       sender_workref=ping_request.work_ref))
        return
