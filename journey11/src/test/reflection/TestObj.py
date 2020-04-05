from typing import Tuple, Dict
from journey11.src.test.reflection.dummyclass import DummyClass


class TestObj:

    def __init__(self):
        self._str1 = "str1"
        self._str2 = "str2"
        return

    def __call__(self, *args, **kwargs):
        return

    @property
    def name(self) -> str:
        return "DummyName"

    def method_no_param(self):
        return

    def method_one_param(self, p1: int) -> None:
        return

    def method_two_param(self, p1: int, p2: Dict) -> Tuple[str, str]:
        return self._str1, self._str2

    def method_class_param(self, p1: DummyClass) -> None:
        return

    @classmethod
    def class_method(cls, p1: Tuple[int, int], p2: Dict) -> Tuple[int, float]:
        return int(1), float(2)
