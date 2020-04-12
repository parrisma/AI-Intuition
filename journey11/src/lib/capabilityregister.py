from enum import Enum, unique


@unique
class CapabilityRegister(Enum):
    ETHER = 0
    POOL = 1
    AGENT = 2

    def __str__(self):
        return self.name

    def __repr__(self):
        return "Capability [{}] with value {}".format(self.__str__(), self.value)
