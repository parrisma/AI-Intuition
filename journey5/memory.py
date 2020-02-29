from copy import deepcopy
from AIIntuition.journeys.journey5.cputype import CPUType
from AIIntuition.journeys.journey5.core import Core
import numpy as np


class Memory:
    # Memory, distribution
    __p_dist_type = {
        CPUType.GPU: [[64, 32, 16], [0.1, 0.8, 0.1]],
        CPUType.GENERAL: [[265, 128, 64], [0.7, 0.2, 0.1]],
        CPUType.BATCH: [[32, 16, 8], [0.1, 0.8, 0.1]]
    }

    def __init__(self,
                 core: Core = None,
                 mem: int = None):
        self._size = mem
        if core is not None:
            _mem_options, _p_dist = Memory.__p_dist_type[core.core_type]
            self._size = _mem_options[np.random.choice(np.arange(0, 3), p=_p_dist)]

        if self._size is None:
            raise ValueError("Must specify a Core or memory size in MB (int)")

    @property
    def size(self) -> int:
        """
        The size of the memory
        :return: The size of the memory in MB
        """
        return deepcopy(self._size)
