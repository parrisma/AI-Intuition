from datetime import datetime
from copy import deepcopy
from journey5.task import Task
from journey5.compute import Compute
from journey5.errorcode import ErrorCode
from journey5.log import Log
from journey5.event import FailureEvent
from journey5.jexception import JException


class OutOfMemoryException(JException):
    """
    Raised when an application cannot secure sufficient memory on the host it is running on.
    """

    def __init__(self,
                 task: Task,
                 compute: Compute):
        """
        Record and Out of Memory issue for Load on Compute
        :param task: The task that required more memory than was available & thus failed
        :param compute: The Compute that was unable to supply the required memory
        """
        self._event_time = time = datetime.now().strftime("%H:%M:%S")
        self._task = task
        self._compute = compute
        self._error_code = ErrorCode.OUT_OF_MEMORY

    def as_string(self,
                  as_feature: bool = False) -> str:
        """
        The exception rendered as string, if as_feature = True then as a feature vector equivalent for use in AL/ML
        context.
        :return: Exception as string
        """
        s = Log.log_message(FailureEvent(self, self._task, self._compute), as_feature)
        return s

    @property
    def task(self) -> Task:
        return self._task

    @property
    def compute(self) -> Compute:
        return self._compute

    @property
    def event_time(self) -> str:
        return deepcopy(self._event_time)

    @property
    def error_code(self) -> int:
        return self._error_code.value
