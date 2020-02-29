from copy import deepcopy
from journey5.core import Core
from journey5.computeprofile import ComputeProfile
from journey5.randomcoreprofile import RandomCoreProfile
from journey5.memory import Memory


class RandomHostProfile(ComputeProfile):

    def __init__(self):
        self._core = Core(RandomCoreProfile())  # ToDo - Host Profile.

    @property
    def core(self) -> Core:
        return deepcopy(self._core)

    @property
    def mem(self) -> Memory:
        return Memory(self._core)
