from enum import Enum
from lib.efforttype import EffortType


class StateEffortMap(Enum):
    FIXED_LOW = 1
    FIXED_HIGH = 2
    FIXED_MID = 3
    RANDOM = 4

    def __init__(self, v):
        self._v = v
        return

    def effort(self):
        return EffortType.effort(self._v)

    def __str__(self):
        return str(self.value)


if __name__ == "__main__":
    for i in range(1, 50):
        print(str(StateEffortMap.RANDOM.effort()))
