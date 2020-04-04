import logging
from queue import Queue
from pubsub import pub
from journey11.src.interface.agent import Agent
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.interface.worknotification import WorkNotification
from journey11.src.interface.taskconsumptionpolicy import TaskConsumptionPolicy
from journey11.src.lib.state import State
from journey11.src.lib.simpleworkrequest import SimpleWorkRequest
from journey11.src.lib.uniquetopic import UniqueTopic


class TestAgent(Agent):
    FAIL_RATE = float(0)

    AGENT_TOPIC_PREFIX = "agent"

    def __init__(self,
                 agent_name: str,
                 start_state: State,
                 end_state: State,
                 capacity: int,
                 task_consumption_policy: TaskConsumptionPolicy):
        """
        """
        super().__init__()
        self._fail_rate = TestAgent.FAIL_RATE
        self._capacity = capacity
        self._work = Queue()
        self._agent_name = agent_name
        self._start_state = start_state
        self._end_state = end_state

        self._num_notification = 0
        self._num_work = 0

        self._unique_topic = None
        self._create_topic_and_subscription()

        self._task_consumption_policy = task_consumption_policy
        return

    def _create_topic_and_subscription(self) -> None:
        """
        Create the unique topic for the agent that it will listen on for work (task) deliveries that it has
        requested from the task-pool
        """
        self._unique_topic = UniqueTopic().topic(TestAgent.AGENT_TOPIC_PREFIX)
        pub.subscribe(self, self._unique_topic)
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
        The unique topic name that SrcSink listens on for activity specific to it.
        :return: The unique SrcSink listen topic name
        """
        return self._unique_topic

    def _do_notification(self,
                         task_notification: TaskNotification):
        """
        callback to Notify agent of a task that needs attention. The agent can request the task be sent to it for
        processing but there is no guarantee as another agent may have already requested the task.
        :param task_notification: The notification event for task requiring attention
        """
        logging.info("{} do_notification for work ref {}".format(self._agent_name, task_notification.work_ref.id))
        self._num_notification += 1
        if self._task_consumption_policy.process_task(task_notification.task_meta):
            if task_notification.originator is not None:
                # request the task ot be sent as work.
                work_request = SimpleWorkRequest(task_notification.work_ref, self)
                pub.sendMessage(topicName=task_notification.originator.topic, arg1=work_request)
                logging.info("{} sent request for work ref {} OK from pool {}".format(self._agent_name,
                                                                                      task_notification.work_ref.id,
                                                                                      task_notification.originator.name))
            else:
                logging.info("{} notification IGNORED by policy for work ref {} OK from pool {}".format(
                    self._agent_name,
                    task_notification.work_ref.id,
                    task_notification.originator.name))
        else:
            self._num_notification -= 1
            logging.info("{} Rx TaskNotification Ignored by Consumption Policy{}".format(self.name,
                                                                                         task_notification.work_ref.id))
        return

    def _do_work(self,
                 work_notification: WorkNotification) -> None:
        """
        Process any out standing tasks associated with the agent.
        """
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
            pub.sendMessage(topicName=work_notification.originator.topic, arg1=work_notification)
            logging.info("{} send task {} to pool {} in state {}".format(self._agent_name,
                                                                         work_notification.task.id,
                                                                         work_notification.originator.name,
                                                                         work_notification.task.state))
        return

    def _add_work_item_to_queue(self,
                                work_notification: WorkNotification) -> None:
        self._work.put(work_notification)
        super().work_notification()
        return

    def reset(self) -> None:
        """
        Return the Actor to the same state at which it was constructed
        """
        return

    def work_to_do(self) -> WorkNotification:
        """
        Are there any tasks associated with the Agent that need working on ?
        :return: A WorkNotification event or None if there is no work to do
        """
        wtd = None
        if not self._work.empty():
            wtd = self._work.get()
            logging.info("{} work_to_do for task ref {}".format(self._agent_name, wtd.work_ref.id))
        else:
            logging.info("{} work_to_do - nothing to do".format(self._agent_name))
        return wtd

    def test_wait_until_done(self) -> None:
        self._work.join()
        return

        # ----- P R O P E R T I E S -----

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
        Hoe many task notifications did teh agent get
        :return: num notifications
        """
        return self._num_notification

    @property
    def num_work(self) -> int:
        """
        Hoe many tasks did the agent work on
        :return: num tasks worked on
        """
        return self._num_work
