from typing import List
from random import shuffle

"""
Iterate randomly and forever over the given list
"""


class InfRndIter:

    def __init__(self,
                 list_to_iter: List[object]):
        if len(list_to_iter) == 0:
            self.__list = None
        else:
            self.__list = list_to_iter
        self.__curr_idx = 0
        self.__rand_idx = None
        self.__gen_rand_idx()

    def __iter__(self):
        return self

    def __next__(self):
        if self.__list is None:
            return None

        if self.__curr_idx == len(self.__rand_idx):
            self.__curr_idx = None

        if self.__curr_idx is None:
            self.__gen_rand_idx()
            self.__curr_idx = 0

        self.__curr_idx += 1

        return self.__list[self.__rand_idx[self.__curr_idx - 1]]

    def __gen_rand_idx(self):
        self.__rand_idx = None
        if self.__list is not None:
            ridx = list(range(0, len(self.__list)))
            shuffle(ridx)
            self.__rand_idx = ridx


if __name__ == "__main__":
    print("Case 1")
    l = range(0, 1)
    ri = InfRndIter(l)
    for x in range(0, 10):
        e = next(ri)
        print(e)

    print("Case 2")
    l = range(0, 20)
    ri = InfRndIter(l)
    for x in range(0, 100):
        e = next(ri)
        print(e)
