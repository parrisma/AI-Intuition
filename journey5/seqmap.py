from copy import deepcopy
import numpy as np


class SeqMap:

    def __init__(self,
                 seq_name: str):

        self._name = seq_name
        self._idx_map = dict()
        self._rev_map = dict()
        self._idx = None
        return

    @property
    def name(self) -> str:
        """
        The name of the sequence mapping
        :return: The name as string for the sequence mapping
        """
        return deepcopy(self._name)

    def value_as_seq_idx(self,
                         value) -> int:
        """
        The value returned as its sequence encoding
        :param value: The value to sequence encode (must be hashable)
        :return: The sequence encoding as an integer
        """
        self._update_idx_map(value=value)
        return self._idx_map[value]

    def __call__(self, *args):
        """
        Class is callable and the behaviour is to convert given value to a sequence idx
        :param args: The object to be mapped to a sequence idx
        :return: The mapped sequence idx of the object given.
        """
        return self.value_as_seq_str(args[0])

    def value_as_seq_str(self,
                         value) -> str:
        """
        The value returned as its sequence encoding in string form
        :param value: The value to sequence encode (must be hashable)
        :return: The sequence encoding as a string
        """
        return str(self.value_as_seq_idx(value=value))

    def _update_idx_map(self,
                        value: object):
        """
        If the given value is not yet know to the sequence mapping then allocate it an index.
        :param value: The value to be allocated a sequence index if it has not yet been allocated one
        """
        if value not in self._idx_map:
            if self._idx is None:
                self._idx = 0
            else:
                self._idx += 1
            self._idx_map[value] = self._idx
            self._update_rev_map(seq_idx=self._idx, value=value)

    def _update_rev_map(self,
                        seq_idx: int,
                        value: object) -> None:
        """
        Maintain the map from value to index
        :param seq_idx: the sequence idx matching the value
        :param value: the value
        """
        if seq_idx not in self._rev_map:
            self._rev_map[seq_idx] = value
        return

    def seq_idx_as_value(self,
                         seq_idx: int) -> object:
        """
        The value that corresponds to the given one hot encoding
        :param seq_idx: The sequence idx to be mapped to its corresponding value
        :return: The value that maps to the given sequence index encoding
        """
        if seq_idx not in self._rev_map:
            raise ValueError('Sequence Idx: ' + str(seq_idx) + ' is not known to sequence map: [' + self._name + ']')

        return self._rev_map[seq_idx]

    def __str__(self):
        """
        Return a string equivalent of the sequence encoder
        :return: String equivalent of the current state of the sequence encoder
        """
        s = 'Sequence Map :[' + self._name + '] Curr items :[' + str(len(self._idx_map)) + ']\n'
        if len(self._rev_map) == 0:
            s += '   No values mapped\n'
        else:
            for k in self._rev_map:
                s += '   ' + str(k) + ' = ' + str(self._rev_map[k]) + '\n'
        return s


if __name__ == "__main__":
    max_test_items = 5
    seq_list = []
    seq_map_test1 = SeqMap(seq_name='Test Sequence Map')

    print(str(seq_map_test1))

    vals = np.random.rand(max_test_items, 1)
    for n in vals:
        try:
            print(str(*n) + ' encoded as ' + seq_map_test1(*n))
            seq_list.append(seq_map_test1.value_as_seq_idx(*n))
        except TypeError as e:
            print(seq_map_test1.__class__.__name__ + ' should be callable ' + str(e))
            raise e
        except Exception as e:
            print('UN-Expected Exception: ' + str(e))

    for n in vals:
        print(str(*n) + ' still encoded as ' + seq_map_test1(*n))

    for seq_item in seq_list:
        v = seq_map_test1.seq_idx_as_value(seq_item)
        print(str(seq_item) + ' is Sequence idx for value:' + str(v))

    try:
        err_seq_map = 9999
        seq_item = seq_map_test1.seq_idx_as_value(err_seq_map)
    except ValueError as e:
        print('Expected Exception: ' + str(e))
    except Exception as e:
        print('UN-Expected Exception: ' + str(e))

    print(str(seq_map_test1))
