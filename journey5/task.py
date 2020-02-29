from abc import ABC, abstractmethod
from enum import Enum, unique
from copy import deepcopy
from typing import List
from typing import Dict
from random import randint

"""
Abstract Base Class for anything that can be considered a compute load e.g. an Application.
"""


class Task(ABC):
    __MAX_TASK_ID = 999999
    __LEN_MAX_TASK = len(str(__MAX_TASK_ID))
    __task_ids = {}
    __all_tasks = {}

    __task_flat = [0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33,
                   0.33, 0.33, 0.33, 0.33, 0.33, 0.33, 0.33]
    __task_st_ed = [0.1, 0.3, 0.8, 0.9, 1, 0.9, 0.6, 0.2, 0.2, 0.1, 0.1, 0.1, 0.2, 0.2, 0.2, 0.3, 0.8, 0.9, 1, 0.9, 0.7,
                    0.3, 0.2, 0.1]
    __task_mid = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.8, 0.9, 1, 0.9, 0.6, 0.2, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,
                  0.1, 0.1, 0.1]
    __task_saw = [0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.2, 0.4, 0.6, 0.9, 0.1, 0.1, 0.2, 0.4,
                  0.6, 0.9, 0.1, 0.1]

    @unique
    class LoadProfile(Enum):
        FLAT = 'Flat'
        START_OF_DAY_END_OF_DAY = 'Sod-Eod'
        MIDDAY_SPIKE = 'Midday'
        SAW_TOOTH = 'Saw'

        def __str__(self):
            return self.value

    __activity_types_l = [LoadProfile.FLAT,
                          LoadProfile.START_OF_DAY_END_OF_DAY,
                          LoadProfile.MIDDAY_SPIKE,
                          LoadProfile.SAW_TOOTH]
    __activity = {
        LoadProfile.FLAT: __task_flat,
        LoadProfile.START_OF_DAY_END_OF_DAY: __task_st_ed,
        LoadProfile.MIDDAY_SPIKE: __task_mid,
        LoadProfile.SAW_TOOTH: __task_saw
    }

    @property
    @abstractmethod
    def id(self) -> str:
        """
        The unique id of the Load.
        :return: Id as string that is unique for all loads.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def task_type(self) -> 'Task.LoadProfile':
        """
        The type of load profile the load exhibits
        :return: String name of the load profile (in set returned by Load.load_types())
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def load_factor(self) -> int:
        """
        The multiple of load placed by teh task on its associated compute resource
        :return: String name of the load profile (in set returned by load_types())
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def core_type(self) -> str:
        """
        The preferred type of compute Core required by the Load (on of set returned by Core.core_types())
        :return: String name of the load profile (in set returned by load_types())
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def current_mem(self) -> int:
        """
        The current memory utilisation of the Load on the Compute resource it is running on
        :return: The amount of memory in MG (int)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def run_time(self) -> int:
        """
        The total number of hours the load has to run for
        :return: The total runtime in hours
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def curr_run_time(self) -> int:
        """
        The number of hours the load has been running for
        :return: The current runtime in hours (0 => load done)
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Is the current load finished processing
        :return: True if Load has finished processing, else False
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def failed(self) -> bool:
        """
        Is the current load in a failed state
        :return: True if Load has failed during processing, else False
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def current_compute(self) -> float:
        """
        The current compute demand of the Load on the Compute resource it is running on
        :return: The amount of compute
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def effective_compute(self) -> float:
        """
        The effective compute demand of the Load on the Compute resource it is running on. This can be greater or
        less then the current_compute if the compute is being supplied by a non preferred core type
        :return: The amount of compute
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def compute_deficit(self) -> float:
        """
        The number of compute cycles behind the task is based on demand and the number of executions
        :return: The amount of compute deficit
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def cost(self) -> float:
        """
        The current cost incurred by the task
        :return: The current task cost
        """
        raise NotImplementedError

    @abstractmethod
    def resource_demand(self,
                        hour_of_day: int) -> List[int]:
        """
        Return the amount of memory and compute needed given the hour of the day.
        :param hour_of_day: Local time - hour of day as integer 0 - 23
        :return: List: Compute Demand, Current Compute, Core Type, Memory Demand for given hour of day
        & current mem utilisation
        """
        raise NotImplementedError

    @abstractmethod
    def task_failure(self,
                     reason: Exception = None) -> None:
        """
        Set the load to failre state
        :param reason: Optional Exception that explains the failre cause.
        :return:
        """

    @property
    @abstractmethod
    def failure_reason(self) -> Exception:
        """
        If the load is in a failed state and a reason exception was given, return the failure exception - None if the
        load is not in a failure state
        :return: The exception, if the node is in a failure state and a reason exception was given.
        """
        raise NotImplementedError

    @abstractmethod
    def execute(self,
                compute_available: float,
                compute_demand: float) -> float:
        """
        Run a compute cycle of the application.
        :param compute_available: The memory allocated to
        :param compute_demand: The compute capacity available to the App
        :return The actual amount of compute taken.
        """
        raise NotImplementedError

    @abstractmethod
    def book_cost(self, cost: float) -> None:
        """
        Record a run cost applied to the task
        :param cost: The cost to be adcded to the current task total cost
        """
        raise NotImplementedError

    @classmethod
    def activity_types(cls) -> List['Task.LoadProfile']:
        """
        List of types of load profile over a 24 hour period
        :return: List of load types as string
        """
        return deepcopy(cls.__activity_types_l)

    @classmethod
    def load_shapes(cls) -> Dict['Task.LoadProfile', List[float]]:
        """
        Dictionary of load profiles
        :return: Dictionary of load profiles keyed by load type
        """
        return deepcopy(cls.__activity)

    @classmethod
    def loads(cls) -> List['Task']:
        """
        List of currently registered loads
        :return: List of registered Loads
        """
        return deepcopy(list(cls.__all_tasks.values()))

    @classmethod
    def __register(cls,
                   id_to_register: str,
                   inst: 'Task') -> None:
        cls.__all_tasks[id_to_register] = inst
        return

    @classmethod
    def gen_id(cls,
               inst: 'Task') -> str:
        """
        Generate a random & unique host id in range 0 to Load.MAX_LOAD_ID that has not already been
        allocated.
        :return: Host id as string with leading zeros, string length always = 5
        """
        rnd_app_id = randint(0, cls.__MAX_TASK_ID)
        while rnd_app_id not in cls.__task_ids:
            rnd_app_id = randint(0, cls.__MAX_TASK_ID)
            cls.__task_ids[rnd_app_id] = True
        _id = str(rnd_app_id).zfill(cls.__LEN_MAX_TASK)
        cls.__register(_id, inst)
        return deepcopy(_id)

    @classmethod
    def all_tasks(cls) -> list:
        """
        Create a deepcopy list of all Loads created at this point in time.
        :return: A list of Loads
        """
        task_list = []
        for k in cls.__all_tasks.keys():
            task_list.append(deepcopy(cls.__all_tasks[k]))
        return task_list
