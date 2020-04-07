import uuid


class UniqueRef:
    def __init__(self):
        self._unique_ref = str(uuid.uuid4()).replace('-', '')

    @property
    def ref(self) -> str:
        return self._unique_ref

    def __str__(self):
        return self._unique_ref

    def __repr__(self):
        return str(self)
