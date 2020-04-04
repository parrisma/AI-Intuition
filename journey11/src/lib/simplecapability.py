from journey11.src.interface.capability import Capability


class SimpleCapability(Capability):

    def __init__(self,
                 capability_name: str):
        super().__init__()
        self._capability_name = capability_name
        return

    def value(self):
        """
        Return the 'value' of the capability
        :return: Capability value
        """
        return self._capability_name

    def _as_str(self) -> str:
        """
        Render the capability as a string
        :return:
        """
        return self._capability_name

    def _equivalent(self,
                    other) -> bool:
        """
        Return true if the two capabilities are equivalent. Where 'equivalent' means separate entities both holding the
        capability would both be able to perform the same type of activity/work.
        :param other: Capability to compare to
        :return: True if capabilities are 'equivalent'
        """
        if isinstance(other.value(), str):
            return other.value() == self._capability_name
        return False
