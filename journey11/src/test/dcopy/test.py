import unittest
from enum import Enum, unique
from journey11.src.lib.dcopy import Dcopy


@unique
class AnEnum(Enum):
    S0 = 0
    S1 = 1
    S2 = 2


class A:
    def __init__(self, a, b, c, d):
        self._a = a
        self.__b = b
        self._ca = c
        self.d = d
        self._ae = "Fixed-A"


class B:
    def __init__(self, a, b, c, d):
        self._a = a
        self.__b = b
        self._cb = c
        self.d = d
        self._be = "Fixed-B"


class Base:
    def __init__(self,
                 s_in: str,
                 b_in: bool,
                 n_in: None,
                 i_in: int,
                 f_in: float):
        self._base_s = s_in
        self._base_b = b_in
        self._base_n = n_in
        self._base_i = i_in
        self._base_f = f_in


class X(Base):
    def __init__(self):
        super().__init__("X Str", True, None, 2281, 3.142)
        self._n = 2
        self._x = 3142
        self.__hidden = 789
        self._z = Z(999, "_999_")
        self._an_enum = AnEnum.S1
        self._l_1 = list()
        self._l_2 = [1, 3, 5]
        self._l_3 = [.2, .4, .6]
        self._l_4 = [.7, .9, .11]
        self._l_5 = [.21, .23, .25, .27]
        self._l_6 = [[1, 2, 3], .4]
        self._l_7 = [True, [Z(1, 2), Z(3, 4)]]
        self._l_8 = [False, [Z(11, 13)]]
        self._d_1 = dict()
        self._d_2 = {'1': 1}
        self._d_3 = {'1': 1, '2': True, '3': 1.2, '4': ['a', 1, True], '5': Z(5, 6)}
        self._d_4 = dict()
        self._d_5 = {'1': 1, '2': True, '3': 1.2, '4': ['a', 1, True], '5': Z(5, 6)}
        return

    @property
    def prop_n(self) -> int:
        return self._n


class Y(Base):
    def __init__(self):
        super().__init__("Y Str", False, None, 4423, 6.284)
        self._n = 1
        self._y = 6284  # Not shared member & will not be copied
        self.__hidden = 345  # Hidden member & will not be copied
        self._z = Z(888, "_888_")
        self._an_enum = AnEnum.S2
        self._l_1 = [7, 8, 9, 0]
        self._l_2 = list()
        self._l_3 = [.1, .3, .5]
        self._l_4 = [.6, .8, .10, .12]
        self._l_5 = [.14, .16]
        self._l_6 = [[11], .7, .13]
        self._l_7 = [False, [Z(8, 9)]]
        self._l_8 = [True, [Z(20, 21), Z(22, 23), Z(24, 25)]]
        self._d_1 = dict()
        self._d_2 = dict()
        self._d_3 = dict()
        self._d_4 = {'9': 9, '8': False, '3': 2.4, '7': ['a', 1, True], '5': Z(5, 6)}
        self._d_5 = {'1': 2, '2': False, '4': ['b', 2, False, 'xray'], '5': Z(1, 9), '6': 'added'}
        return


class Z:
    def __init__(self, a_in, b_in):
        self._a = a_in
        self._b = b_in

    def __str__(self):
        return "Z:(_a {} : _b {})".format(self._a, self._b)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._a == other._a and self._b == other._b
        else:
            return False


class TestDcopy(unittest.TestCase):
    def test_fails(self):
        scenarios = [[int(0), float(0)],
                     [AnEnum.S1, bool(True)],
                     [list(), dict()],
                     [[int(0), float(0)], [int(0), int(0)]],
                     [list(), Z(1, 2)],
                     [Z(1.0, 2), Z(3, 4)],
                     [Z([1, 2, 3], "Hi"), Z([1, 2.0], "Lo")]
                     ]
        for scenario in scenarios:
            src, tgt = scenario
            with self.assertRaises(TypeError):
                _ = Dcopy.deep_corresponding_copy(src=src, tgt=tgt)
        return

    def test_simple(self):
        scenarios = [[int(678), int(0), int(678)],
                     [[1, 2], [6, 7], [1, 2]],
                     [[1, 2], [6, 7, 8], [1, 2, 8]],
                     [[1, 2, 3, 4], [6, 7, 8], [1, 2, 3, 4]],
                     [dict(), dict(), dict()],
                     [{1: 2}, {1: 3}, {1: 2}],
                     [{1: 2, 2: 3}, {1: 2, 2: 5, 3: 4}, {1: 2, 2: 3, 3: 4}],
                     [{1: [Z({1: 2, 2: 3}, [3, 4, 5])], 3: "4", 4: True},
                      {1: [Z({1: 3, 3: 4}, [1, 4, 5, 4])], 3: "5", 4: False},
                      {1: [Z({1: 2, 2: 3, 3: 4}, [3, 4, 5, 4])], 3: "4", 4: True}],
                     [Z(Z(Z(Z(Z(1, 2), 3), 4), 5), 6), Z(Z(Z(Z(Z(9, 8), 7), 6), 5), 4),
                      Z(Z(Z(Z(Z(1, 2), 3), 4), 5), 6)],
                     [[[1, 2], 3], [[4, 5], 6], [[1, 2], 3]],
                     [[[[[[float(0)]]]]], [[[[[float(1)]]]]], [[[[[float(0)]]]]]]
                     ]
        for scenario in scenarios:
            src, tgt, expected = scenario
            self.assertEqual(expected, Dcopy.deep_corresponding_copy(src=src, tgt=tgt))
        return

    def test_fields_fwd(self):
        # A - > B
        src = A(1, 2.0, "3", AnEnum.S0)
        tgt = B(4, 5.0, "6", AnEnum.S2)
        tgt_unmod = B(4, 5.0, "6", AnEnum.S2)
        actual = Dcopy.deep_corresponding_copy(src, tgt)
        self.assertEqual(src._a, actual._a)  # Corresponding & updated
        self.assertEqual(getattr(tgt_unmod, "_{}__b".format(type(tgt_unmod).__name__)),
                         getattr(actual, "_{}__b".format(type(actual).__name__)))  # .__b hidden & not updated
        self.assertEqual(tgt_unmod._cb, actual._cb)  # Not corresponding & not updated
        self.assertEqual(src.d, actual.d)  # Corresponding & updated
        self.assertEqual(tgt._be, actual._be)  # Not Corresponding & const on __init__

    def test_fields_rev(self):
        # B -> A
        src = B(4, 5.0, "6", AnEnum.S2)
        tgt = A(1, 2.0, "3", AnEnum.S0)
        tgt_unmod = A(1, 2.0, "3", AnEnum.S0)
        actual = Dcopy.deep_corresponding_copy(src, tgt)
        self.assertEqual(src._a, actual._a)  # Corresponding & updated
        self.assertEqual(getattr(tgt_unmod, "_{}__b".format(type(tgt_unmod).__name__)),
                         getattr(actual, "_{}__b".format(type(actual).__name__)))  # .__b hidden & not updated
        self.assertEqual(tgt_unmod._ca, actual._ca)  # Not corresponding & not updated
        self.assertEqual(src.d, actual.d)  # Corresponding & updated
        self.assertEqual(tgt._ae, actual._ae)  # Not Corresponding & const on __init__
        return

    def test_complex_nested(self):
        actual = Dcopy.deep_corresponding_copy(X(), Y())
        expected = X()
        target_unmodified = Y()

        # Top Level - with over lap
        self.assertEqual(expected._n, actual._n)
        self.assertEqual(expected._an_enum, actual._an_enum)

        # Top Level - no over lap or hidden
        self.assertEqual(target_unmodified._y, actual._y)  # ._y not shared, should not be overridden
        self.assertEqual(getattr(target_unmodified, "_{}__hidden".format(type(target_unmodified).__name__)),
                         getattr(actual, "_{}__hidden".format(type(actual).__name__)))  # ._hidden should be same

        # Contained object
        self.assertEqual(expected._z._a, actual._z._a)
        self.assertEqual(expected._z._b, actual._z._b)

        # Inherited
        self.assertEqual(expected._base_s, actual._base_s)
        self.assertEqual(expected._base_b, actual._base_b)
        self.assertEqual(expected._base_n, actual._base_n)
        self.assertEqual(expected._base_i, actual._base_i)
        self.assertEqual(expected._base_f, actual._base_f)

        # Simple Lists
        self.assertEqual(target_unmodified._l_1, actual._l_1)
        self.assertEqual(expected._l_2, actual._l_2)
        self.assertEqual(expected._l_3, actual._l_3)
        self.assertEqual([.7, .9, .11, .12], actual._l_4)
        self.assertEqual(expected._l_5, actual._l_5)
        self.assertEqual([[1, 2, 3], .4, .13], actual._l_6)

        # Heterogeneous lists with objects
        self.assertEqual(expected._l_7, actual._l_7)
        self.assertEqual([False, [Z(11, 13), Z(22, 23), Z(24, 25)]], actual._l_8)

        # Simple dictionaries
        self.assertEqual(expected._d_1, actual._d_1)
        self.assertEqual(expected._d_2, actual._d_2)

        # Complex dictionaries
        self.assertEqual(expected._d_3, actual._d_3)
        self.assertEqual(target_unmodified._d_4, actual._d_4)
        self.assertEqual({'1': 1, '2': True, '3': 1.2, '4': ['a', 1, True, 'xray'], '5': Z(5, 6), '6': 'added'},
                         actual._d_5)
        return


if __name__ == "__main__":
    unittest.main()
