from copy import deepcopy
from typing import List
import math
import numpy as np
from AIIntuition.journeys.journey5.cputype import CPUType
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.taskprofile import TaskProfile
from AIIntuition.journeys.journey5.randomtaskprofile import RandomTaskProfile
from AIIntuition.journeys.journey5.util import Util


class App(Task):

    def __init__(self,
                 task_profile: TaskProfile):
        """
        Create an application with a profile according to the prob distribution of demand
        for Core Type, Memory and expected load profile
        :return:
        """
        self._id = Task.gen_id(self)
        self._max_mem_demand = task_profile.max_mem
        self._memory_volatility = task_profile.mem_volatility
        self._core_demand = task_profile.cpu_type
        self._load_profile = task_profile.load_profile
        self._load_shape = task_profile.load_shape
        self._run_time_ask = task_profile.run_time
        self._core_load = task_profile.task_load

        # Properties that change during execution
        self._cost = 0  # for the task lifetime , does not reset

        self._run_time_in_elapse_hours = None
        self._compute_deficit = None
        self._current_mem = None
        self._current_comp = None
        self._effective_comp = None
        self._failed = None
        self._fail_reason = None
        self._reset()

    def _reset(self) -> None:
        """
        Set the application to it's initial launch state
        :return:
        """
        self._run_time_in_elapse_hours = self._run_time_ask
        self._compute_deficit = 0
        self._current_mem = 0
        self._current_comp = 0
        self._effective_comp = 0
        self._failed = False
        self._fail_reason = None
        return

    @property
    def id(self) -> str:
        return deepcopy(self._id)

    @property
    def task_type(self) -> Task.LoadProfile:
        return deepcopy(self._load_profile)

    @property
    def core_type(self) -> CPUType:
        return deepcopy(self._core_demand)

    @property
    def done(self) -> bool:
        """
        Is the current load finished processing
        :return: True if Load has finished processing, else False
        """
        return self._run_time_in_elapse_hours == 0

    @property
    def failed(self) -> bool:
        """
        Is the current load in a failed state
        :return: True if Load has failed during processing, else False
        """
        return deepcopy(self._failed)

    @property
    def current_mem(self) -> int:
        """
        The current memory utilisation of the Load on the Compute resource it is running on
        :return: The amount of memory in MG (int)
        """
        return deepcopy(self._current_mem)

    @property
    def current_compute(self) -> int:
        """
        The current compute demand of the Load on the Compute resource it is running on
        :return: The amount of compute
        """
        return deepcopy(self._current_comp)

    @property
    def effective_compute(self) -> int:
        """
        The effective compute demand of the Load on the Compute resource it is running on. This can be greater or
        less then the current_compute if the compute is being supplied by a non preferred core type
        :return: The amount of compute
        """
        return deepcopy(self._current_comp)

    @property
    def compute_deficit(self) -> int:
        """
        The number of compute cycles behind the task is based on demand and the number of executions
        :return: The amount of compute deficit
        """
        return deepcopy(self._compute_deficit)

    @property
    def run_time(self) -> int:
        """
        The total number of hours the load has to run for
        :return: The total runtime in hours
        """
        return deepcopy(self._run_time_ask)

    @property
    def curr_run_time(self) -> int:
        """
        The number of hours the load has been running for
        :return: The current runtime in hours (0 => load done)
        """
        return deepcopy(self._run_time_in_elapse_hours)

    @property
    def load_factor(self) -> int:
        """
        The multiple of load placed by the task on its associated compute resource
        :return: String name of the load profile (in set returned by load_types())
        """
        return deepcopy(self._core_load)

    @property
    def cost(self) -> float:
        """
        The life to date cost of executing the task, this includes the cost of all failed attempts
        :return: The life to date cost of running the task.
        """
        return deepcopy(self._cost)

    # ToDo: return immutable tuple not a list
    def resource_demand(self,
                        local_hour_of_day: int) -> List[int]:
        """
        Return the amount of memory and compute needed given the hour of the day.
        :param local_hour_of_day: Local time - hour of day as integer 0 - 23
        :return: List: Compute Demand, Current Compute, Core Type, Memory Demand for given hour of day
        & current mem utilisation
        """
        cm = self.current_mem
        cc = self.current_compute
        self._current_comp = self.__compute_demand(local_hour_of_day)
        self._current_mem = self.__memory_demand(local_hour_of_day)
        return [self.current_compute,
                cc,
                self.core_type,
                self.current_mem,
                cm
                ]

    def task_failure(self,
                     reason: Exception = None) -> None:
        """
        Set the load to failre state
        :param reason: Optional Exception that explains the failre cause.
        :return:
        """
        self._failed = True
        self._fail_reason = reason
        self._reset()
        return

    @property
    def failure_reason(self) -> Exception:
        """
        If the load is in a failed state and a reason exception was given, return the failure exception - None if the
        load is not in a failure state
        :return: The exception, if the node is in a failure state and a reason exception was given.
        """
        if not self._failed:
            r = None
        else:
            r = self._fail_reason
        return r

    def execute(self,
                compute_available: float,
                compute_demand: float) -> float:
        """
        Run a compute cycle of the application.
        :param compute_available: The memory allocated to
        :param compute_demand: The compute capacity available to the App
        :return The actual amount of compute taken.
        """
        if not self.done:
            self._run_time_in_elapse_hours -= 1
            self._compute_deficit = min(1e6, max(0.0, (compute_demand - compute_available)))
        return compute_demand - self._compute_deficit

    def book_cost(self, cost: float) -> None:
        """
        Record a run cost applied to the task
        :param cost: The cost to be adcded to the current task total cost
        """
        self._cost += cost
        return

    def __memory_demand(self,
                        local_hour_of_day: int) -> int:
        """
        Given the hour of the day what is the memory demand of the App.
        :param local_hour_of_day: local hour of day
        :return: Memory demand in GB
        """
        new_mem = self._max_mem_demand * self._load_shape[local_hour_of_day]
        new_mem *= (1 + np.random.uniform(-self._memory_volatility, +self._memory_volatility))
        new_mem = math.ceil(new_mem)
        new_mem = min(new_mem, self._max_mem_demand)
        new_mem = max(new_mem, 0)
        self._current_mem = new_mem
        return new_mem

    def __compute_demand(self,
                         local_hour_of_day: int) -> float:
        """
        What is the total compute demand given the hour of the day.
        :param local_hour_of_day: hour_of_day: Local time - hour of day as integer 0 - 23
        :return: Compute demand as integer (units * 1 hour) - where 1 unit = 1 x GPU, Compute etc
        """
        compute_demand = (self._core_load *
                          self._load_shape[local_hour_of_day]
                          ) + self._compute_deficit
        return compute_demand

    def __str__(self):
        return ''.join((self.id, ': ',
                        'profile: ', str(self.task_type), ': ',
                        'core type: ', str(self.core_type), ': ',
                        'Mem(Max,Curr):',
                        str(self.current_mem), ' - Progress:',
                        Util.to_pct((self.run_time - self.curr_run_time),
                                    self.run_time), '%'
                        )
                       )


if __name__ == "__main__":
    app = None
    for i in range(1, 100):
        app = App(RandomTaskProfile())
    for a in Task.loads():
        print(a)
    for h in range(0, 23):
        app.execute(h, 1000, 1000, 1)
        print(app)
