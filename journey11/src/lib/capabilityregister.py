from enum import Enum, unique


@unique
class CapabilityRegister(Enum):
    ETHER = 0
    POOL = 1
    AGENT = 2
    S0S1 = 3
    S1S2 = 4
    S2S3 = 5
    S3S4 = 6
    S4S5 = 7
    S5S6 = 8
    S6S7 = 9
    S7S8 = 10
    S8S9 = 11

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Capability [{}] with value {}".format(self.__str__(), self.value)
