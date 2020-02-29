from copy import deepcopy
from journey5.core import Core
from journey5.computeprofile import ComputeProfile
from journey5.memory import Memory


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
