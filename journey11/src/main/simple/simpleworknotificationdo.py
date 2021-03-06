from journey11.src.interface.task import Task
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class SimpleWorkNotificationDo(WorkNotificationDo):
    # Annotation
    _work_ref: UniqueWorkRef
    _task: Task
    _originator: SrcSink
    _source: SrcSink

    def __init__(self,
                 unique_work_ref: UniqueWorkRef,
                 task: Task,
                 originator: SrcSink,
                 source: SrcSink):
        self._work_ref = unique_work_ref
        self._task = task
        self._originator = originator
        self._source = source

    @property
    def work_ref(self) -> UniqueWorkRef:
        """
        The unique work reference for this notification
        :return: The work reference
        """
        return self._work_ref

    @property
    def task(self) -> Task:
        """
        The task the notification event relates to
        :return: The task
        """
        return self._task

    @property
    def originator(self) -> SrcSink:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._originator

    @property
    def source(self) -> SrcSink:
        """
        The task_pool the notification event relates to
        :return: The task pool
        """
        return self._source

    def __str__(self):
        """
        Render as string
        :return: String rendering of class instance
        """
        return "Work Notification Do task: {} from originator {} with source {}".format(self._task.id,
                                                                                        self._originator.name,
                                                                                        self._source.name)
