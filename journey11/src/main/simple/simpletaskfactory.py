from typing import List
from journey11.src.interface.task import Task
from journey11.src.interface.taskfactory import TaskFactory
from journey11.src.interface.taskgenerationpolicy import TaskGenerationPolicy
from journey11.src.lib.state import State
from journey11.src.main.simple.simpletask import SimpleTask


class SimpleTaskFactory(TaskFactory):

    def __init__(self,
                 start_state: State,
                 task_gen_policy: TaskGenerationPolicy):
        self._tesk_gen_policy = task_gen_policy
        self._start_state = start_state
        return

    def generate(self) -> List[Task]:
        """
        Generate one or more tasks
        :return: List of newly generated tasks.
        """
        efforts = self._tesk_gen_policy.num_to_generate()
        tasks = list()
        for effort in efforts:
            tasks.append(SimpleTask(effort=effort, start_state=self._start_state))
        return tasks
