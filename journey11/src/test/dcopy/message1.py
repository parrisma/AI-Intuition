from typing import List
from journey11.src.test.dcopy.state import State
from journey11.src.test.dcopy.task import Task


class Message1:
    # Annotation needed by Copy to Protbuf as type hints for some conversions
    _field: str
    _state: State
    _tasks: List[Task]
    _strings: List[str]
    _double: float
    _float: float
    _int32: int
    _int64: int
    _bool: bool
    _bytes: bytes

    def __init__(self, **kwargs):
        self._field = kwargs.get('field', str())
        self._state = kwargs.get('state', State.S1)
        self._tasks = kwargs.get('tasks', list())
        self._strings = kwargs.get('strings', list())
        self._double = kwargs.get('_double', float())
        self._float = kwargs.get('_float', float())
        self._int32 = kwargs.get('_int32', int())
        self._int64 = kwargs.get('_int64', int())
        self._bool = kwargs.get('_bool', int())
        self._bytes = kwargs.get('_bytes', bytes())
        return

    def __str__(self):
        return "Message1:(field: {} state:{}, tasks:{} strings:{})".format(self._field, self._state, str(self._tasks),
                                                                           str(self._strings))

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self._field == other._field and self._state == other._state and self._double == other._double and \
                    self._float == other._float and self._int32 == other._int32 and self._int64 == other._int64 and \
                    self._bool == other._bool and self._bytes == other._bytes:
                if len(self._tasks) == len(other._tasks):
                    for s, o in zip(self._tasks, other._tasks):
                        if s != o:
                            return False
            if len(self._strings) == len(other._strings):
                for s, o in zip(self._strings, other._strings):
                    if s != o:
                        return False
            return True
        else:
            return False
