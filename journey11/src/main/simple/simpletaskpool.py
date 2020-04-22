import threading
import logging
from typing import List
from pubsub import pub
from journey11.src.interface.taskpool import TaskPool
from journey11.src.interface.workrequest import WorkRequest
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.interface.srcsinkpingnotification import SrcSinkPingNotification
from journey11.src.interface.worknotificationfinalise import WorkNotificationFinalise
from journey11.src.interface.srcsinkping import SrcSinkPing
from journey11.src.interface.capability import Capability
from journey11.src.interface.ether import Ether
from journey11.src.lib.state import State
from journey11.src.lib.capabilityregister import CapabilityRegister
from journey11.src.main.simple.simpletasknotification import SimpleTaskNotification
from journey11.src.main.simple.simpletaskmetadata import SimpleTaskMetaData
from journey11.src.main.simple.simpleworknotificationdo import SimpleWorkNotificationDo
from journey11.src.main.simple.simpleworknotificationfinalise import SimpleWorkNotificationFinalise
from journey11.src.main.simple.simplesrcsinkpingnotification import SimpleSrcSinkNotification
from journey11.src.main.simple.simplesrcsinkping import SimpleSrcSinkPing
from journey11.src.main.simple.simplecapability import SimpleCapability


class SimpleTaskPool(TaskPool):
    _POOL_CAPABILITY = SimpleCapability(str(CapabilityRegister.POOL))

    def __init__(self,
                 name: str,
                 pool_capabilities: List[Capability] = None):
        super().__init__(name)
        self._task_pool = dict()
        self._pool_lock = threading.RLock()
        self._len = 0
        self._name = name
        self._ping_factor_threshold = float(1)
        self._capabilities = list()
        self.set_pool_capabilities(pool_capabilities)
        return

    def __del__(self):
        """
        Set running False, which will stop timer resets etc.
        """
        super().__del__()

    def terminate_all(self) -> None:
        """
        Terminate all activity, locks, threads, timers etc
        """
        self.__del__()
        return

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
                  work_notification: WorkNotificationDo) -> None:
        """
        Add a task to the task pool which will cause it to be advertised via the relevant topic unless the task
        is in it's terminal state in which case it is sent back to its ultimate source
        :param work_notification: The task to be added
        """
        if work_notification.task.state == work_notification.task.process_end_state():
            logging.warning("{} expected finalised rather than do as task complete & in end state".format(
                work_notification.source.name))
            work_notification_finalise = SimpleWorkNotificationFinalise.finalise_factory(work_notification)
            logging.info("{} converted {} to finalised & processed".format(self.name,
                                                                           work_notification_finalise.work_ref.id))
            pub.sendMessage(topicName=self.topic,
                            notification=work_notification_finalise)
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
                to_pub = [work_request.originator.topic, SimpleWorkNotificationDo(unique_work_ref=work_request.work_ref,
                                                                                  task=work.task,
                                                                                  originator=work.originator,
                                                                                  source=self)]

        if to_pub is not None:
            topic, notification = to_pub
            logging.info("{} sent task {} to {}".format(self.name,
                                                        notification.work_ref.id,
                                                        notification.originator.name))
            pub.sendMessage(topicName=topic, notification=notification)
        else:
            logging.info("{} had NO task {} to send to {}".format(self.name,
                                                                  work_request.work_ref.id,
                                                                  work_request.originator.name))

        return

    def _do_pub(self) -> None:
        """
        Check for any pending tasks and advertise or re-advertise them on the relevant topic
        """
        to_pub = list()
        with self._pool_lock:
            for ref in self._task_pool.keys():
                work_ref, work = self._task_pool[ref]
                topic = self.topic_for_capability(work.task.state)
                stn = SimpleTaskNotification(unique_work_ref=work_ref,
                                             task_meta=SimpleTaskMetaData(work.task.id),
                                             originator=self)
                to_pub.append([work_ref, topic, stn, work.task.id])

        for pub_event in to_pub:
            ref, topic, notification, task_id = pub_event
            logging.info("{} stored & advertised task {} on {} = {}".format(self.name, task_id, topic, ref.id))
            pub.sendMessage(topicName=topic, notification=notification)

        return

    def _do_manage_presence(self) -> None:
        """
        Ensure that we are known on the ether.
        """
        if self._get_recent_ether_address() is None:
            logging.info("{} not linked to Ether - sending discovery Ping".format(self.name))
            pub.sendMessage(topicName=Ether.back_plane_topic(),
                            notification=SimpleSrcSinkPing(sender_srcsink=self,
                                                           required_capabilities=[
                                                               SimpleCapability(str(CapabilityRegister.ETHER))]))
        return

    def _do_srcsink_ping_notification(self,
                                      ping_notification: SrcSinkPingNotification) -> None:
        """
        Handle a ping response from a srcsink
        :param: The srcsink notification
        """
        logging.info("{} RX ping response for {}".format(self.name, ping_notification.src_sink.name))
        if ping_notification.src_sink.topic != self.topic:
            # Don't count ping response from our self.
            for srcsink in ping_notification.responder_address_book:
                self._update_addressbook(srcsink=srcsink)
        return

    def _do_srcsink_ping(self,
                         ping_request: SrcSinkPing) -> None:
        """
        Handle a ping response from a srcsink
        :param: The srcsink notification
        """
        logging.info("{} RX ping request for {}".format(self.name, ping_request.sender_srcsink.name))
        # Don't count pings from our self.
        if ping_request.sender_srcsink.topic != self.topic:
            # Note the sender is alive
            self._update_addressbook(ping_request.sender_srcsink)
            if Capability.equivalence_factor(ping_request.required_capabilities,
                                             self.capabilities) >= self._ping_factor_threshold:
                pub.sendMessage(topicName=ping_request.sender_srcsink.topic,
                                notification=SimpleSrcSinkNotification(responder_srcsink=self,
                                                                       address_book=[self],
                                                                       sender_workref=ping_request.work_ref))
        return

    def _do_work_finalise(self,
                          work_notification_final: WorkNotificationFinalise) -> None:
        """
        Take receipt of the given completed work item that was initiated from this agent and do any
        final processing.
        """
        logging.info("{} Rx Finalised task {} from source {} in state {}".format(self.name,
                                                                                 work_notification_final.work_ref.id,
                                                                                 work_notification_final.originator.name,
                                                                                 work_notification_final.task.state))
        # Send to Originator for closure
        pub.sendMessage(topicName=work_notification_final.originator.topic,
                        notification=work_notification_final)
        return

    def topic_for_capability(self,
                             state: State) -> str:
        """
        The topic string on which tasks needing work in that state are published on
        :param state: The state for which the topic is required
        :return: The topic string for the given state
        """
        return "topic-{}".format(str(state.id()))

    def set_pool_capabilities(self,
                              additional_capabilities: List[Capability] = None) -> None:
        """ Set the given capabilities for the Agent and add the base capabilities that all Agents have.
        :param additional_capabilities: Optional capabilities to add to the base capabilities
        """
        with self._pool_lock:
            if self._POOL_CAPABILITY not in self._capabilities:
                self._capabilities.append(self._POOL_CAPABILITY)
            if additional_capabilities is not None:
                for c in additional_capabilities:
                    if c not in self._capabilities:
                        self._capabilities.append(c)
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

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        """
        The number of tasks currently in the pool
        :return: The number of tasks in the pool
        """
        return self._len
