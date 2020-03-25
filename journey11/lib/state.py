from enum import Enum, unique


@unique
class State(Enum):
    S0 = 0
    S1 = 1
    S2 = 2
    S3 = 3
    S4 = 4
    S5 = 5
    S6 = 6
    S7 = 7
    S8 = 8
    S9 = 9

    def id(self):
        return self.value

    def __str__(self) -> str:
        return "State:{}".format(self.value)
