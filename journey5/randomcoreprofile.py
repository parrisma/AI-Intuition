import numpy as np
from copy import deepcopy
from AIIntuition.journeys.journey5.cputype import CPUType
from AIIntuition.journeys.journey5.coreprofile import CoreProfile


class RandomCoreProfile(CoreProfile):
    """
    Create a new compute core - the core type is allocated given the supplied probability distribution
    p_dist_core_types: a 1 by 3 probability distribution over core_types [gpu, cpu, batch]
    """
    _p_dist_core_types = [.2, .5, .3]

    # Cores, distribution
    _p_dist_type = {
        CPUType.GPU: [[16, 8, 4], [0.1, 0.8, 0.1]],
        CPUType.GENERAL: [[8, 4, 2], [0.7, 0.2, 0.1]],
        CPUType.BATCH: [[4, 2, 1], [0.1, 0.8, 0.1]]
    }

    def __init__(self):
        self._core_type = CPUType.cpu_types()[np.random.choice(np.arange(0, 3), p=self._p_dist_core_types)]
        _nc, _p_dist = self._p_dist_type[self._core_type]
        self._core_count = _nc[np.random.choice(np.arange(0, 3), p=_p_dist)]

    @property
    def core_type(self) -> CPUType:
        return deepcopy(self._core_type)

    @property
    def core_count(self) -> CPUType:
        return deepcopy(self._core_count)
