class Task:
    _task_name: str
    _task_id: int

    def __init__(self, **kwargs):
        self._task_name = kwargs.get('task_name', str())
        self._task_id = kwargs.get('task_id', int())
        return

    @property
    def task_name(self) -> str:
        return self._task_name

    @property
    def task_id(self) -> int:
        return self._task_id

    def __str__(self):
        return "Task:(task_name:{} task_id:{})".format(self._task_name, self._task_id)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._task_id == other._task_id and self._task_name == other._task_name
        else:
            return False
