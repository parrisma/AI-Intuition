import random
from state import State


class EffortType:
    __LOW = [10]
    __HIGH = [60]
    __MID = [30, 40]
    __RAND = [10, 20, 30, 40, 50, 60]

    _v_to_f = {
        1: 'fixed_low',
        2: 'fixed_high',
        3: 'fixed_mid',
        4: 'random_choice'
    }

    @classmethod
    def fixed_low(cls, _: State) -> int:
        return random.choice(cls.__LOW)

    @classmethod
    def fixed_high(cls, _: State) -> int:
        return random.choice(cls.__HIGH)

    @classmethod
    def fixed_mid(cls, _: State) -> int:
        return random.choice(cls.__MID)

    @classmethod
    def random_choice(cls, _: State) -> int:
        return random.choice(cls.__RAND)

    @classmethod
    def effort(cls,
               v: int):
        return getattr(cls, cls._v_to_f[v])(None)
