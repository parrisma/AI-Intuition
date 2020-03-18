import threading
from pubsub import pub
from journey11.interface.taskpool import TaskPool
from journey11.interface.task import Task
from journey11.lib.state import State
from journey11.lib.simpletasknotification import SimpleTaskNotification


class SimpleTaskPool(TaskPool):

    def __init__(self,
                 name: str):
        self._task_pools = dict()
        self._pool_lock = threading.Lock()
        self._len = 0
        self._name = name

    @property
    def name(self) -> str:
        """
        The name of the task pool
        :return: The name of the task pool as string
        """
        return self._name

    def put_task(self,
                 task: Task) -> None:
        """
        Add a task to the task pool which will cause it to be advertised via the relevant topic unless the task
        is in it's terminal state.
        :param task: The task to be added
        """
        topic = self.topic_for_state(task.state)
        if topic not in self._task_pools:
            with self._pool_lock:
                self._task_pools[topic] = [dict(), threading.Lock()]

        pool, lock = self._task_pools[topic]
        with lock:
            if task.id not in pool:
                pool[task.id] = task
                self._len += 1

        pub.sendMessage(topicName=topic, arg1=SimpleTaskNotification(task, self))

        return

    def get_task(self,
                 task: Task) -> Task:
        """
        Pull a task out of the pool so it can be processed
        :param task: The task to get, None is returned if the task cannot be found (no longer in the pool)
        """
        task_result = None
        for topic in self._task_pools.keys():
            pool, lock = self._task_pools[topic]
            if task.id in pool:
                with lock:
                    task_result = pool[task.id]
                    del pool[task.id]
                    self._len -= 1
        return task_result

    def topic_for_state(self,
                        state: State) -> str:
        """
        The topic string on which tasks needing work in that state are published on
        :param state: The state for which the topic is required
        :return: The topic string for the given state
        """
        return "topic-{}".format(str(state.id()))

    def __str__(self) -> str:
        """
        String dump of the current pool state
        :return: A string representation of teh task pool.
        """

        # Use locks so we see a consistent view of the task_pool
        #
        s = "Task Pool [{}]\n".format(self._name)
        with self._pool_lock:
            for topic in self._task_pools.keys():
                s += "   Topic ({})\n".format(topic)
                pool, lock = self._task_pools[topic]
                with lock:
                    for task in pool:
                        s += "       Task <{}>\n".format(str(task))
        return s

    def __len__(self):
        """
        The number of tasks currently in the pool
        :return: The number of tasks in the pool
        """
        return self._len
