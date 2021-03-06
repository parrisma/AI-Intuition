from journey11.src.interface.task import Task
from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.worknotificationinitiate import WorkNotificationInitiate
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class SimpleWorkNotificationInitiate(WorkNotificationInitiate):

    def __init__(self,
                 task: Task,
                 originator: SrcSink,
                 source: SrcSink = None):
        self._task = task
        if source is None:
            self._source = originator
        else:
            self._source = source
        self._originator = originator
        self._work_ref = UniqueWorkRef(suffix=str(task.id), prefix=originator.name)
        return

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
        fmt = "Work Notification Finalise ref: {} for task {} from originator {} with source {}"
        return fmt.format(self._work_ref,
                          self._task.id,
                          self._originator.name,
                          self._source.name)

    def __repr__(self):
        return self.__str__()
