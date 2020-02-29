from typing import List
from copy import deepcopy
from AIIntuition.journeys.journey5.cputype import CPUType
from AIIntuition.journeys.journey5.task import Task
from AIIntuition.journeys.journey5.taskprofile import TaskProfile


class FixedTaskProfile(TaskProfile):

    def __init__(self,
                 max_mem: int,
                 mem_vol: float,
                 cpu_type: CPUType,
                 load_profile: Task.LoadProfile,
                 load_factor: int,
                 run_time: int):
        self._max_mem = max_mem
        self._mem_vol = mem_vol
        self._cpu_type = cpu_type
        self._load_factor = load_factor
        self._load_profile = load_profile
        self._load_shape = Task.load_shapes()[self.load_profile]
        self._run_time = run_time

    @property
    def max_mem(self) -> int:
        return deepcopy(self._max_mem)

    @property
    def mem_volatility(self) -> float:
        return deepcopy(self._mem_vol)

    @property
    def cpu_type(self) -> CPUType:
        return deepcopy(self._cpu_type)

    @property
    def task_load(self) -> int:
        return deepcopy(self._load_factor)

    @property
    def load_profile(self) -> Task.LoadProfile:
        return deepcopy(self._load_profile)

    @property
    def load_shape(self) -> List[float]:
        return deepcopy(self._load_shape)

    @property
    def run_time(self) -> int:
        return deepcopy(self._run_time)
