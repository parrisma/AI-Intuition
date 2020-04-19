from journey11.src.interface.taskmetadata import TaskMetaData


class SimpleTaskMetaData(TaskMetaData):

    def __init__(self,
                 task_id: int):
        self._id = task_id
        return

    @property
    def task_id(self) -> int:
        return self._id

    def __str__(self) -> str:
        return str(self._id)
