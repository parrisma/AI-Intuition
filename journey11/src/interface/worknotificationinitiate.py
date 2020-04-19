from abc import abstractmethod
from journey11.src.interface.notification import Notification
from journey11.src.interface.task import Task
from journey11.src.lib.purevirtual import purevirtual


class WorkNotificationInitiate(Notification):

    @property
    @abstractmethod
    @purevirtual
    def task(self) -> Task:
        """
        The task to work on
        :return: The task
        """
        pass
