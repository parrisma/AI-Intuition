from journey11.src.interface.capability import Capability


class SimpleCapability(Capability):
    # Annotation
    _uuid: str
    _capability_name: str

    def __init__(self,
                 uuid: str,
                 capability_name: str):
        """
        Represent the capability of an agent to contribute to the completion of a task
        :param uuid: The system wide unique UUID of the capability
        :param capability_name: The capability
        """
        super().__init__()
        self._capability_name = capability_name
        self._uuid = uuid
        return

    def id(self) -> str:
        """
        Return the system wide unique uuid
        :return: UUID of the capability.
        """
        return self._uuid

    def value(self) -> str:
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
        return "Capability: {} := {}".format(self._uuid, self._capability_name)

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
