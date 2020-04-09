from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.task import Task
from journey11.src.interface.worknotificationdo import WorkNotificationDo
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class TestWorkNotificationDo(WorkNotificationDo):
    _task_id = 1
    _src = 1

    def __init__(self):
        self._unique_sig = UniqueWorkRef(task_id=str(TestWorkNotificationDo._task_id),
                                         originator_id=str(TestWorkNotificationDo._src))
        TestWorkNotificationDo._task_id += 1
        TestWorkNotificationDo._src += 1

    @property
    def task(self) -> Task:
        return None

    @property
    def source(self) -> SrcSink:
        return None

    @property
    def work_ref(self) -> UniqueWorkRef:
        return self._unique_sig

    @property
    def originator(self) -> SrcSink:
        return None

    def __str__(self):
        return "{} - ref: {}".format(self.__class__.__name__, str(self._unique_sig))

    def __repr__(self):
        return str(self)