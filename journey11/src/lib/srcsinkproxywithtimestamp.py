import datetime
from journey11.src.interface.srcsinkproxy import SrcSinkProxy


class SrcSinkProxyWithTimeStamp:
    def __init__(self,
                 time_stamp: datetime,
                 src_sink_proxy: 'SrcSinkProxy'):
        self._time_stamp = time_stamp
        self._src_sink_proxy = src_sink_proxy
        return

    @property
    def srcsink(self) -> 'SrcSinkProxy':
        return self._src_sink_proxy

    @property
    def time_stamp(self) -> datetime:
        return self._time_stamp

    @time_stamp.setter
    def time_stamp(self,
                   t: datetime) -> None:
        self._time_stamp = t
        return

    def __str__(self):
        return "{} @ {:%d %m %Y : %I %M %S %f }".format(self._src_sink_proxy.name, self.time_stamp)

    def __repr__(self):
        return self.__str__()
