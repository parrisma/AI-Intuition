from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.taskmetadata import TaskMetaData
from journey11.src.interface.tasknotification import TaskNotification
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class TestTaskNotification(TaskNotification):
    _task_id = 1
    _src = 1

    def __init__(self):
        self._unique_sig = UniqueWorkRef(subject_name=str(TestTaskNotification._task_id),
                                         work_item_ref=str(TestTaskNotification._src))
        TestTaskNotification._task_id += 1
        TestTaskNotification._src += 1

    @property
    def work_ref(self) -> UniqueWorkRef:
        return self._unique_sig

    @property
    def task_meta(self) -> TaskMetaData:
        return None

    @property
    def originator(self) -> SrcSink:
        return None

    def __str__(self):
        return "{} - ref: {}".format(self.__class__.__name__, str(self._unique_sig))

    def __repr__(self):
        return str(self)
