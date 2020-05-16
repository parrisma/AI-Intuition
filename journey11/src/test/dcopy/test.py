import unittest
import logging
from enum import Enum, unique
from journey11.src.lib.dcopy.copy import Copy
from journey11.src.lib.loggingsetup import LoggingSetup
from journey11.src.test.dcopy.state import State
from journey11.src.test.dcopy.task import Task
from journey11.src.test.dcopy.message1 import Message1
from journey11.src.test.dcopy.pb_message1_pb2 import PBMessage1


@unique
class AnEnumInt(Enum):
    S0 = 0
    S1 = 1
    S2 = 2


@unique
class AnEnumStr(Enum):
    S0 = "0"
    S1 = "1"
    S2 = "2"


@unique
class AnEnumWithMembers(Enum):
    S0 = (1, 2)
    S1 = (2, 3)
    S2 = (3, 4)

    def __init__(self, p1, p2):
        self._p1 = p1
        self._p2 = p2
        return

    @property
    def func(self):
        return self._p1 * self._p2


class A:
    def __init__(self, a, b, c, d):
        self._a = a
        self.__b = b
        self._ca = c
        self.d = d
        self._ae = "Fixed-A"

    def __str__(self):
        return "A:(_a:{} __b:{} _ca:{} d:{} _ae{}".format(self._a, self.__b, self._ca, self.d, self._ae)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._a == other._a and self.__b == other.__b and self._ca == other._ca and self.d == other.d and self._ae == other._ae
        else:
            return False


class B:
    def __init__(self, a, b, c, d):
        self._a = a
        self.__b = b
        self._cb = c
        self.d = d
        self._be = "Fixed-B"

    def __str__(self):
        return "B:(_a:{} __b:{} _cb:{} d:{} _ae{}".format(self._a, self.__b, self._cb, self.d, self._be)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._a == other._a and self.__b == other.__b and self._cb == other._cb and self.d == other.d and self._be == other._be
        else:
            return False


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
        self._an_enum = AnEnumInt.S1
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
        self._an_enum = AnEnumInt.S2
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

    @classmethod
    def setUpClass(cls):
        LoggingSetup()

    def test_fails(self):
        logging.info("Test failure cases for type mismatch")
        scenarios = [[int(0), float(0)],
                     [AnEnumInt.S1, bool(True)],
                     [AnEnumStr.S2, int(0)],
                     [list(), dict()],
                     [[int(0), float(0)], [int(0), int(0)]],
                     [list(), Z(1, 2)],
                     [Z(1.0, 2), Z(3, 4)],
                     [Z([1, 2, 3], "Hi"), Z([1, 2.0], "Lo")]
                     ]
        for scenario in scenarios:
            src, tgt = scenario
            with self.assertRaises(TypeError):
                _ = Copy.deep_corresponding_copy(src=src, tgt=tgt)
        return

    def test_simple_obj(self):
        logging.info("Test simple, un-nested object")
        src = Z(A(1, 2, 3, 4), B(5, 6, 7, 8))
        tgt = Z(A(10, 12, 13, 14), B(15, 16, 17, 18))
        tgt = Copy.deep_corresponding_copy(src=src, tgt=tgt)
        self.assertEqual(src, tgt)
        return

    def test_enum(self):
        logging.info("Test enum specifics")
        # Pass case
        src = Z(AnEnumInt.S1, AnEnumStr.S2)
        tgt = Z(AnEnumInt.S0, AnEnumStr.S0)
        tgt = Copy.deep_corresponding_copy(src, tgt)
        self.assertEqual(tgt, src)

        # Pass case reverse as it's valid to copy a str Enum over an Int Enum
        src = Z(AnEnumInt.S1, AnEnumStr.S2)
        tgt = Z(AnEnumStr.S0, AnEnumInt.S0)  # Reverse int/str type Enum
        tgt = Copy.deep_corresponding_copy(src, tgt)
        self.assertEqual(tgt, src)
        return

    def test_enum_with_members(self):
        src = Z(AnEnumWithMembers.S0, AnEnumInt.S0)
        tgt = Z(AnEnumWithMembers.S1, AnEnumInt.S2)
        tgt = Copy.deep_corresponding_copy(src, tgt)
        self.assertEqual(tgt, src)
        self.assertEqual((1 * 2), src._a.func)
        return

    def test_enum_to_value_type(self):
        # Pass case, target types align with value type
        src = Z(AnEnumInt.S2, AnEnumStr.S1)
        tgt = Z(int(3142), "3142")
        tgt = Copy.deep_corresponding_copy(src, tgt)
        self.assertEqual(tgt._a, src._a.value)
        self.assertEqual(tgt._b, src._b.value)

        # Fail case target type not same as value type
        src = Z(AnEnumInt.S2, AnEnumStr.S1)
        tgt = Z("3142", int(3142))
        with self.assertRaises(TypeError):
            _ = Copy.deep_corresponding_copy(src=src, tgt=tgt)

        return

    def test_simple(self):
        logging.info("Test simple base types and collections")
        scenarios = [[int(678), int(0), int(678)],
                     [[1, 2], [6, 7], [1, 2]],
                     [[1, 2], [6, 7, 8], [1, 2, 8]],
                     [[1, 2, 3, 4], [6, 7, 8], [1, 2, 3, 4]],
                     [dict(), dict(), dict()],
                     [{1: 2}, {1: 3}, {1: 2}],
                     [{1: 2, 2: 3}, {1: 2, 2: 5, 3: 4}, {1: 2, 2: 3, 3: 4}],
                     [{1: [Z({1: 2, 2: 3}, [3, 4, 5])], 3: "4", 4: True},
                      {1: [Z({1: 3, 3: 4}, [1, 4, 5, 4])], 3: "5", 4: False, 7: AnEnumInt.S1},
                      {1: [Z({1: 2, 2: 3, 3: 4}, [3, 4, 5, 4])], 3: "4", 4: True, 7: AnEnumInt.S1}],
                     [Z(Z(Z(Z(Z(1, 2), 3), 4), 5), 6), Z(Z(Z(Z(Z(9, 8), 7), 6), 5), 4),
                      Z(Z(Z(Z(Z(1, 2), 3), 4), 5), 6)],
                     [[[1, 2], 3], [[4, 5], 6], [[1, 2], 3]],
                     [[[[[[float(0)]]]]], [[[[[float(1)]]]]], [[[[[float(0)]]]]]]
                     ]
        for scenario in scenarios:
            src, tgt, expected = scenario
            self.assertEqual(expected, Copy.deep_corresponding_copy(src=src, tgt=tgt))
        return

    def test_fields_fwd(self):
        logging.info("Test simple object to object with only partial member field overlap A -> B")
        # A - > B
        src = A(1, 2.0, "3", AnEnumInt.S0)
        tgt = B(4, 5.0, "6", AnEnumInt.S2)
        tgt_unmod = B(4, 5.0, "6", AnEnumInt.S2)
        actual = Copy.deep_corresponding_copy(src, tgt)
        self.assertEqual(src._a, actual._a)  # Corresponding & updated
        self.assertEqual(getattr(tgt_unmod, "_{}__b".format(type(tgt_unmod).__name__)),
                         getattr(actual, "_{}__b".format(type(actual).__name__)))  # .__b hidden & not updated
        self.assertEqual(tgt_unmod._cb, actual._cb)  # Not corresponding & not updated
        self.assertEqual(src.d, actual.d)  # Corresponding & updated
        self.assertEqual(tgt._be, actual._be)  # Not Corresponding & const on __init__
        return

    def test_fields_rev(self):
        logging.info("Test simple object to object with only partial member field overlap B -> A")
        # B -> A
        src = B(4, 5.0, "6", AnEnumInt.S2)
        tgt = A(1, 2.0, "3", AnEnumInt.S0)
        tgt_unmod = A(1, 2.0, "3", AnEnumInt.S0)
        actual = Copy.deep_corresponding_copy(src, tgt)
        self.assertEqual(src._a, actual._a)  # Corresponding & updated
        self.assertEqual(getattr(tgt_unmod, "_{}__b".format(type(tgt_unmod).__name__)),
                         getattr(actual, "_{}__b".format(type(actual).__name__)))  # .__b hidden & not updated
        self.assertEqual(tgt_unmod._ca, actual._ca)  # Not corresponding & not updated
        self.assertEqual(src.d, actual.d)  # Corresponding & updated
        self.assertEqual(tgt._ae, actual._ae)  # Not Corresponding & const on __init__
        return

    def test_complex_nested(self):
        logging.info("Test complex nested object, with base types, collections, Enum etc")
        actual = Copy.deep_corresponding_copy(X(), Y())
        expected = X()
        target_unmodified = Y()

        # Top Level - with over lap
        self.assertEqual(expected._n, actual._n)
        self.assertEqual(expected._an_enum, actual._an_enum)

        # Top Level - no over lap or hidden
        self.assertEqual(target_unmodified._y, actual._y)  # ._y not shared, should not be overridden
        self.assertEqual(getattr(target_unmodified, "_{}__hidden".format(type(target_unmodified).__name__)),
                         getattr(actual,
                                 "_{}__hidden".format(type(actual).__name__)))  # ._hidden should be same

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

    def test_protobuf_copy(self):
        """
        Copy to and back from a Protobuf type and ensure the original object is the same as the copy.
        :return:
        """
        logging.info("Test copy to/from a protobuf type")
        message1 = Message1(field='Message-687',
                            state=State.S2,
                            tasks=[Task(task_name="Task-1", task_id=1), Task(task_name="Task-2", task_id=2)],
                            strings=["A", "2", "c", "4", "D"],
                            _double=3.142,
                            _float=6.284,
                            _int32=496,
                            _int64=8128,
                            _bool=True,
                            _bytes=b'A Byte String')

        pb_message1 = PBMessage1()
        actual = Copy.deep_corresponding_copy(message1, pb_message1)
        try:
            actual.SerializeToString()
        except Exception:
            self.fail("Profbuf object invalid after copy as cannot serialize")
        message2 = Message1()
        final = Copy.deep_corresponding_copy(actual, message2)
        self.assertEqual(final, message1)

        return

    def test_prune(self):
        logging.info("Test prune sunshine cases")
        z1a = 1
        z1b = 2
        z2a = 3
        z2b = 4
        scenarios = [[None, z1a, z1b],
                     [[None], z1a, z1b],
                     ['', z1a, z1b],
                     ['_a', z2a, z1b],
                     [['a', 'a_', 'x', 'b', 'b_'], z1a, z1b],
                     [['_a'], z2a, z1b],
                     [['_a', '_a'], z2a, z1b]]
        for p, expected_a, expected_b in scenarios:
            z1 = Z(z1a, z1b)
            z2 = Z(z2a, z2b)
            actual = Copy.deep_corresponding_copy(src=z1, tgt=z2, prune=p)
            self.assertEqual(actual._a, expected_a)
            self.assertEqual(actual._b, expected_b)
        return

    def test_prune_fails(self):
        logging.info("Test prune failure cases")
        z1a = 1
        z1b = 2
        z2a = 3
        z2b = 4
        scenarios = [1, [1], bool, [bool], 3.142, [3.142], ['_b', 123]]
        for p in scenarios:
            z1 = Z(z1a, z1b)
            z2 = Z(z2a, z2b)
            with self.assertRaises(TypeError):
                _ = Copy.deep_corresponding_copy(src=z1, tgt=z2, prune=p)
        return


if __name__ == "__main__":
    unittest.main()
