import datetime
from journey11.src.interface.srcsink import SrcSink


class SrcSinkWithTimeStamp:
    def __init__(self,
                 time_stamp: datetime,
                 srcsink: 'SrcSink'):
        self._time_stamp = time_stamp
        self._src_sink = srcsink
        return

    @property
    def srcsink(self) -> 'SrcSink':
        return self._src_sink

    @property
    def time_stamp(self) -> datetime:
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self,
                   t: datetime) -> None:
        self._time_stamp = t
        return

    def __str__(self):
        return "{} @ {:%d %m %Y : %I %M %S %f }".format(self._src_sink.name, self.time_stamp)

    def __repr__(self):
        return self.__str__()
