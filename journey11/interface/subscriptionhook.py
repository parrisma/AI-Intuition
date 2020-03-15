from abc import ABC, abstractmethod
from journey11.interface.task import Task
from journey10.lib.simpletask import SimpleTask


class SubscriptionHook(ABC):

    def __call__(self,
                 task: Task):
        return self.notify(task=task)

    @abstractmethod
    def notify(self,
               task: Task) -> None:
        """
        :param task: A task that tests positive to 'of_interest'
        """
        pass


class SimpleSubscriptionHook(SubscriptionHook):
    def notify(self,
               task: Task) -> None:
        """
        :param task: A task that tests positive to 'of_interest'
        """
        print("Ping: " + str(task.id))
        return


if __name__ == "__main__":
    tasks = list()
    for _ in range(5):
        tasks.append(SimpleTask)
    pass
