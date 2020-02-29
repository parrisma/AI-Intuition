from copy import deepcopy
from AIIntuition.journeys.journey5.coreprofile import CoreProfile
from AIIntuition.journeys.journey5.cputype import CPUType


class FixedCoreProfile(CoreProfile):

    def __init__(self,
                 core_type: CPUType,
                 core_count: int):
        self._core_type = core_type
        self._core_count = core_count

    @property
    def core_type(self) -> CPUType:
        return deepcopy(self._core_type)

    @property
    def core_count(self) -> int:
        return deepcopy(self._core_count)
