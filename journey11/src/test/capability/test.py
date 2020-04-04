import unittest
from journey11.src.lib.simplecapability import SimpleCapability


class TestCapability(unittest.TestCase):

    def test_simple(self):
        capability_name = "DummyCapability1"
        test_capability = SimpleCapability(capability_name)
        self.assertEqual(capability_name, test_capability.value())
        self.assertEqual(capability_name, str(test_capability))
        return

    def test_equality_same_type(self):
        capability_name_one = "DummyCapability1"
        capability_name_two = "DummyCapability2"
        test_capability_1 = SimpleCapability(capability_name_one)
        test_capability_2 = SimpleCapability(capability_name_one)
        test_capability_3 = SimpleCapability(capability_name_two)
        self.assertEqual(True, test_capability_1 == test_capability_2)
        self.assertEqual(True, test_capability_1 != test_capability_3)
        return

    def test_equality_diff_type(self):
        capability_name_one = "DummyCapability1"
        test_capability_1 = SimpleCapability(capability_name_one)
        self.assertEqual(True, test_capability_1 != capability_name_one)
        self.assertEqual(True, test_capability_1 != int(1))
        return


if __name__ == "__main__":
    unittest.main()
