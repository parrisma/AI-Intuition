from copy import deepcopy
import numpy as np


class OneHot:

    def __init__(self,
                 one_hot_name: str,
                 max_items: int):
        if max_items <= 0:
            raise ValueError('One Hot map must contain at least one item, requested max is: ' + str(max_items))

        self._name = one_hot_name
        self._max_items = max_items
        self._idx_map = dict()
        self._rev_map = dict()
        self._idx = None
        return

    @property
    def max_items(self) -> int:
        """
        The number of items encoded by this one hot mapping
        :return: The maximum number of encodable items
        """
        return deepcopy(self._max_items)

    @property
    def name(self) -> str:
        """
        The name of the one hot mapping
        :return: The name as string for the one hot mapping
        """
        return deepcopy(self._name)

    def value_as_one_hot(self,
                         value) -> np.ndarray:
        """
        The value returned as its one hot encoding
        :param value: The value to one hot encode (must be hashable)
        :return: The one hot encoding as a numpy array
        """
        self._update_idx_map(value=value)
        one_hot = np.zeros(self.max_items)
        one_hot[self._idx_map[value]] = float(1)
        self._update_rev_map(one_hot=one_hot, value=value)
        return one_hot

    def value_as_one_hot_str(self,
                             value) -> str:
        """
        The value returned as its one hot encoding in string form
        :param value: The value to one hot encode (must be hashable)
        :return: The one hot encoding as a string
        """
        return np.array_str(self.value_as_one_hot(value=value))

    def _update_idx_map(self,
                        value: object):
        """
        If the given value is not yet know to the one hot mapping then allocate it an index. If all indexes are
        used because we have reached the maximum throw a ValueError exception.
        :param value: The value to be allocated a one hot index if it has not yet been allocated one
        """
        if value not in self._idx_map:
            if self._idx is None:
                self._idx = 0
            else:
                if self._idx == self._max_items - 1:
                    raise ValueError(
                        'One Hot [' + self._name + '] can only encode a max of: ' + str(
                            self.max_items) + ' different values')
                self._idx += 1
            self._idx_map[value] = self._idx

    def _update_rev_map(self,
                        one_hot: np.ndarray,
                        value: object):
        one_hot_as_str = np.array_str(one_hot)
        if one_hot_as_str not in self._rev_map:
            self._rev_map[one_hot_as_str] = value
        return

    def one_hot_as_value(self,
                         one_hot: np.ndarray) -> object:
        """
        The value that corresponds to the given one hot encoding
        :param one_hot: The one_hot to be mapped to its corresponding value
        :return: The value that maps to the given one hot encoding
        """
        one_hot_as_str = np.array_str(one_hot)
        if one_hot_as_str not in self._rev_map:
            raise ValueError('One Hot: ' + one_hot_as_str + ' is not known to one hot map: [' + self._name + ']')

        return self._rev_map[np.array_str(one_hot)]

    def __str__(self):
        """
        Return a string equivalent of the one hot encoder
        :return: String equivalent of the current state of the map
        """
        s = 'OneHot Map :[' + self._name + '] Max items :[' + str(self.max_items) + ']\n'
        if len(self._rev_map) == 0:
            s += '   No values mapped\n'
        else:
            for k in self._rev_map:
                s += '   ' + str(k) + ' = ' + str(self._rev_map[k]) + '\n'
        return s


if __name__ == "__main__":
    max_test_items = 5
    one_hot_list = []
    one_hot_test1 = OneHot(max_items=max_test_items, one_hot_name='Test One Hot Map')

    print(str(one_hot_test1))

    for n in np.random.rand(max_test_items, 1):
        one_hot_list.append(one_hot_test1.value_as_one_hot(*n))
        print(str(*n) + ' encoded as ' + np.array_str(one_hot_list[-1]))

    for one_hot_item in one_hot_list:
        v = one_hot_test1.one_hot_as_value(one_hot_item)
        print(np.array_str(one_hot_item) + ' is one hot for value:' + str(v))

    try:
        one_hot_item = one_hot_test1.value_as_one_hot(9999)
    except ValueError as e:
        print('Expected Exception: ' + str(e))
    except Exception as e:
        print('UN-Expected Exception: ' + str(e))

    try:
        err_one_hot = np.zeros(max_test_items)
        one_hot_item = one_hot_test1.one_hot_as_value(err_one_hot)
    except ValueError as e:
        print('Expected Exception: ' + str(e))
    except Exception as e:
        print('UN-Expected Exception: ' + str(e))

    print(str(one_hot_test1))
