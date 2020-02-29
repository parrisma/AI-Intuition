from copy import deepcopy
from AIIntuition.journeys.journey5.cputype import CPUType
from AIIntuition.journeys.journey5.coreprofile import CoreProfile
from AIIntuition.journeys.journey5.randomcoreprofile import RandomCoreProfile

"""
Capture the characteristics of compute Core types (GPU, CPU etc) 
"""


class Core:
    __core_equivalency = {
        # Demand Core + Actual Core
        CPUType.GPU + CPUType.GPU: 1.0,
        CPUType.GPU + CPUType.GENERAL: 0.1,
        CPUType.GPU + CPUType.BATCH: 0.05,
        CPUType.GENERAL + CPUType.GENERAL: 1.0,
        CPUType.GENERAL + CPUType.GPU: 2.0,
        CPUType.GENERAL + CPUType.BATCH: 0.25,
        CPUType.BATCH + CPUType.BATCH: 1.0,
        CPUType.BATCH + CPUType.GENERAL: 2.0,
        CPUType.BATCH + CPUType.GPU: 4.0
    }

    __core_cost = {
        CPUType.GPU: 1.0,
        CPUType.GENERAL: 0.25,
        CPUType.BATCH: 0.1
    }

    def __init__(self,
                 core_profile: CoreProfile):
        """
        Create a new compute core - as defined by the passed Core Profile.
        """
        self._core_type = core_profile.core_type
        self._core_count = core_profile.core_count

    def __str__(self):
        return str(self._core_count) + ' of: ' + str(self._core_type.value)

    @property
    def core_type(self) -> CPUType:
        return deepcopy(self._core_type)

    @property
    def num_core(self) -> int:
        return deepcopy(self._core_count)

    @property
    def core_cost(self) -> float:
        return deepcopy(self.__core_cost[self._core_type])

    @classmethod
    def core_compute_equivalency(cls,
                                 required_core_type: CPUType,
                                 given_core_type: CPUType) -> float:
        """
        What is the compute equivalency between the core asked for by a Load and the available core.
        :param required_core_type: The core type required by a Load
        :param given_core_type: The core type available from a Compute source
        :return: The factor to translate from required to given efficacy
        """
        mapping = required_core_type + given_core_type
        if mapping not in cls.__core_equivalency:
            raise ValueError('Core equivalency for [' + mapping + '] does not exist')
        return cls.__core_equivalency[mapping]


if __name__ == "__main__":
    rcp = RandomCoreProfile()
    c = Core(rcp)
    print(c)
    eq = c.core_compute_equivalency(CPUType.GPU, CPUType.GENERAL)
    print(str(eq))
