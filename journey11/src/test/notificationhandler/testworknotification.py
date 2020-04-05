from journey11.src.interface.srcsink import SrcSink
from journey11.src.interface.task import Task
from journey11.src.interface.worknotification import WorkNotification
from journey11.src.lib.uniqueworkref import UniqueWorkRef


class TestWorkNotification(WorkNotification):
    _task_id = 1
    _src = 1

    def __init__(self):
        self._unique_sig = UniqueWorkRef(task_id=str(TestWorkNotification._task_id),
                                         originator_id=str(TestWorkNotification._src))
        TestWorkNotification._task_id += 1
        TestWorkNotification._src += 1

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
