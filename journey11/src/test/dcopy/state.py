from enum import EnumMeta, IntEnum, unique


class DefaultStateEnumMeta(EnumMeta):
    default = object()

    def __call__(cls, value=default, *args, **kwargs):
        if value is DefaultStateEnumMeta.default:
            return next(iter(cls))
        return super().__call__(value, *args, **kwargs)


class State(IntEnum, metaclass=DefaultStateEnumMeta):
    S1 = 0
    S2 = 1
    S3 = 2
