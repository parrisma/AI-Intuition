from copy import deepcopy
from AIIntuition.journeys.journey5.core import Core
from AIIntuition.journeys.journey5.computeprofile import ComputeProfile
from AIIntuition.journeys.journey5.randomcoreprofile import RandomCoreProfile
from AIIntuition.journeys.journey5.memory import Memory


class RandomHostProfile(ComputeProfile):

    def __init__(self):
        self._core = Core(RandomCoreProfile())  # ToDo - Host Profile.

    @property
    def core(self) -> Core:
        return deepcopy(self._core)

    @property
    def mem(self) -> Memory:
        return Memory(self._core)
