from copy import deepcopy
from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.computeprofile import ComputeProfile
from AIIntuition.journeys.journey5.memory import Memory


class FixedHostProfile(ComputeProfile):

    def __init__(self,
                 mem: int,
                 core: Core):
        self._mem = Memory(mem=mem)
        self._core = core

    @property
    def core(self) -> Core:
        return deepcopy(self._core)

    @property
    def mem(self) -> Memory:
        return deepcopy(self._mem)
