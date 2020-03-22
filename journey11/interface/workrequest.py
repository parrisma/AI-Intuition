from abc import ABC, abstractmethod
from enum import Enum, unique
from journey11.interface.srcsink import SrcSink
from journey11.lib.purevirtual import purevirtual
from journey11.interface.taskmetadata import TaskMetaData


class WorkRequest(ABC):
    @property
    @abstractmethod
    @purevirtual
    def task_meta_data(self) -> TaskMetaData:
        """
        The task being requested from the SrcSink
        :return: The task id being requested
        """
        pass

    @property
    @abstractmethod
    @purevirtual
    def src_sink(self) -> SrcSink:
        """
        The SrcSink participant that originating (sender) the request
        :return: The originating (sender) SrcSink of teh request
        """
        pass
