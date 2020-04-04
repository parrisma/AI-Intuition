import threading
import logging
from pubsub import pub
from journey11.src.interface.taskpool import TaskPool
from journey11.src.lib.state import State
from journey11.src.lib.simpletasknotification import SimpleTaskNotification
from journey11.src.interface.workrequest import WorkRequest
from journey11.src.interface.worknotification import WorkNotification
from journey11.src.lib.uniquetopic import UniqueTopic
from journey11.src.lib.simpletaskmetadata import SimpleTaskMetaData
from journey11.src.lib.simpleworknotification import SimpleWorkNotification


class SimpleTaskPool(TaskPool):
    POOL_TOPIC_PREFIX = "TaskPool"

    def __init__(self,
                 name: str):
        super().__init__()
        self._task_pool = dict()
        self._pool_lock = threading.Lock()
        self._len = 0
        self._name = name
        self._unique_topic = None
        self._create_topic_and_subscription()

        self._pub_timer_wait_in_seconds = 0.1
        self._running = True
        self.pub_timer_reset()

        return

    def __del__(self):
        """
        Set running False, which will stop timer resets etc.
        """
        super().__del__()
        self._running = False

    def terminate_all(self) -> None:
        """
        Terminate all activity, locks, threads, timers etc
        """
        self.__del__()
        return

    def _create_topic_and_subscription(self) -> None:
        """
        Create the unique topic for the agent that it will listen on for work (task) deliveries that it has
        requested from the task-pool
        """
        self._unique_topic = UniqueTopic().topic(SimpleTaskPool.POOL_TOPIC_PREFIX)
        pub.subscribe(self, self._unique_topic)

    @property
    def topic(self) -> str:
        """
        The unique topic name that SrcSink listens on for activity specific to it.
        :return: The unique SrcSink listen topic name
        """
        return self._unique_topic

    @property
    def name(self) -> str:
        """
        The name of the task pool
        :return: The name of the task pool as string
        """
        return self._name

    def _put_task(self,
                  work_notification: WorkNotification) -> None:
        """
        Add a task to the task pool which will cause it to be advertised via the relevant topic unless the task
        is in it's terminal state in which case it is sent back to its ultimate source
        :param work_notification: The task to be added
        """
        if work_notification.task.state == work_notification.task.process_end_state():
            pub.sendMessage(topicName=work_notification.source.topic, arg1=work_notification)
            logging.info("{} sent finalised task {} to {}".format(self.name,
                                                                  work_notification.task.id,
                                                                  work_notification.source.name))
        else:
            with self._pool_lock:
                self._task_pool[work_notification.work_ref.id] = [work_notification.work_ref, work_notification]
                self._len += 1
        return

    def _get_task(self,
                  work_request: WorkRequest) -> None:
        """
        Send the requested task to the consumer if the task has not already been sent to a consumer
        :param work_request: The details of the task and the consumer
        """
        logging.info("{} received request for work ref {} from {}".format(self.name,
                                                                          work_request.work_ref.id,
                                                                          work_request.originator.name))
        to_pub = None
        with self._pool_lock:
            ref_id = work_request.work_ref.id
            if ref_id in self._task_pool:
                ref, work = self._task_pool[ref_id]
                del self._task_pool[ref_id]
                self._len -= 1
                to_pub = [work_request.originator.topic, SimpleWorkNotification(unique_work_ref=work_request.work_ref,
                                                                                task=work.task,
                                                                                originator=self,
                                                                                source=work.source)]

        if to_pub is not None:
            topic, arg1 = to_pub
            pub.sendMessage(topicName=topic, arg1=arg1)
            logging.info("{} sent task {} to {}".format(self.name,
                                                        arg1.task.id,
                                                        work_request.originator.name))
        else:
            logging.info("{} had NO task {} to send to {}".format(self.name,
                                                                  work_request.work_ref.id,
                                                                  work_request.originator.name))

        return

    def _do_pub(self,
                pub_notification: TaskPool.PubNotification) -> None:
        """
        Check for any pending tasks and advertise or re-advertise them on the relevant topic
        :param pub_notification: The publication notification closure
        """
        to_pub = list()
        with self._pool_lock:
            for ref in self._task_pool.keys():
                work_ref, work = self._task_pool[ref]
                topic = self.topic_for_state(work.task.state)
                stn = SimpleTaskNotification(unique_work_ref=work_ref,
                                             task_meta=SimpleTaskMetaData(work.task.id),
                                             originator=self)
                to_pub.append([work_ref, topic, stn, work.task.id])

        for pub_event in to_pub:
            ref, topic, arg1, task_id = pub_event
            pub.sendMessage(topicName=topic, arg1=arg1)
            logging.info("{} stored & advertised task {} on {} = {}".format(self.name, task_id, topic, ref.id))

        self.pub_timer_reset()
        return

    def topic_for_state(self,
                        state: State) -> str:
        """
        The topic string on which tasks needing work in that state are published on
        :param state: The state for which the topic is required
        :return: The topic string for the given state
        """
        return "topic-{}".format(str(state.id()))

    def pub_timer_reset(self) -> None:
        """
        Reset the timer that calls _do_pub() method which in turn is responsible for sending notification
        event for any un claimed tasks.
        """
        if self._running:
            threading.Timer(self._pub_timer_wait_in_seconds, self, [TaskPool.PubNotification()]).start()
        return

    def __str__(self) -> str:
        """
        String dump of the current pool state
        :return: A string representation of teh task pool.
        """

        # Use locks so we see a consistent view of the task_pool
        #
        s = "Task Pool [{}]\n".format(self._name)
        with self._pool_lock:
            for topic in self._task_pool.keys():
                s += "   Topic ({})\n".format(topic)
                pool, lock = self._task_pool[topic]
                with lock:
                    for task in pool:
                        s += "       Task <{}>\n".format(str(task))
        return s

    def __len__(self):
        """
        The number of tasks currently in the pool
        :return: The number of tasks in the pool
        """
        return self._len
