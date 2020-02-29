import numpy as np
from typing import List
from copy import deepcopy
from journey5.cputype import CPUType
from journey5.task import Task
from journey5.taskprofile import TaskProfile


class RandomTaskProfile(TaskProfile):
    __pdist_compute_core_demand = [0.2, 0.6, 0.2]
    __memory_asks = [128, 64, 32, 16, 8, 2, 1]
    __psidt_memory_demand = [0.05, 0.1, 0.25, 0.3, 0.15, 0.1, 0.05, ]
    __pdist_loads = [.25, .25, .25, .25]

    def __init__(self):
        self._max_mem = self.__memory_asks[np.random.choice(np.arange(0, 7), p=self.__psidt_memory_demand)]
        self._mem_vol = np.random.uniform(0, 0.1)
        self._cpu_type = CPUType.cpu_types()[np.random.choice(np.arange(0, 3), p=self.__pdist_compute_core_demand)]
        pt = np.random.choice(np.arange(0, 4), p=self.__pdist_loads)
        self._load_profile = Task.activity_types()[pt]
        self._load_shape = Task.load_shapes()[self.load_profile]
        self._run_time = np.ceil(np.random.uniform(0.0, 72.0))
        self._load = np.random.choice(np.arange(0, 10))

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
        return deepcopy(self._load)

    @property
    def load_profile(self) -> Task.LoadProfile:
        return deepcopy(self._load_profile)

    @property
    def load_shape(self) -> List[float]:
        return deepcopy(self._load_shape)

    @property
    def run_time(self) -> int:
        return deepcopy(self._run_time)
