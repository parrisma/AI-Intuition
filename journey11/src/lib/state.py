import logging
from typing import List
from enum import EnumMeta, Enum, unique


class DefaultStateEnumMeta(EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        if value is DefaultStateEnumMeta.default:
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)


@unique
class State(Enum, metaclass=DefaultStateEnumMeta):
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

    @classmethod
    def range(cls,
              start_state: 'State',
              end_state: 'State') -> List['State']:
        rev = False
        if start_state.value > end_state.value:
            rev = True
            st = end_state
            ed = start_state
        else:
            rev = False
            st = start_state
            ed = end_state

        rng = list()
        for _, member in State.__members__.items():
            if st.value <= member.value <= ed.value:
                rng.append(member)
        if rev:
            rng = rng[::-1]

        return rng

    def __str__(self) -> str:
        return "State:{}".format(self.value)

    def __add__(self, other):
        if not isinstance(other, int):
            msg = ""
            logging.critical(msg)
            raise ValueError(msg)

        res = None
        if other == 0:
            res = self
        elif other > 0:
            rng = self.range(self, State.S9)
            if other > len(rng) - 1:
                res = State.S9
            else:
                res = rng[other]
        else:
            rng = self.range(State.S0, self)[::-1]
            other = abs(other)
            if other > len(rng) - 1:
                res = State.S0
            else:
                res = rng[other]
        return res

    def __radd__(self, other):
        return self.__add__(other)
