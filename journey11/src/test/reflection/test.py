from typing import Dict, Tuple
import unittest
from journey11.src.lib.reflection import Reflection
from journey11.src.test.reflection.TestObj import TestObj
from journey11.src.test.reflection.dummyclass import DummyClass
from journey11.src.test.reflection.dummyclass2 import DummyClass2


class TestReflection(unittest.TestCase):

    def setUp(self) -> None:
        self.test_obj = TestObj()

    def test_simple_method_no_param(self):
        # Method exists, so no exception expected
        #
        try:
            Reflection.check_method_exists(object_to_reflect_on=self.test_obj,
                                           method_name="method_no_param",
                                           expected_param_types=Reflection.no_params,
                                           exception_on_error=True)
        except Exception as e:
            self.fail("Unexpected Exception in method check: [{}]".format(str(e)))

        # Method does not exist, so exception expected
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_method_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'method_name': "name_of_method_not_in_class",
                             'expected_param_types': Reflection.no_params,
                             'exception_on_error': True}
                          )
        return

    def test_method_one_param(self):
        # Method & Type exist so no exception expected
        #
        try:
            Reflection.check_method_exists(self.test_obj, "method_one_param", [int])
        except Exception as e:
            self.fail("Unexpected Exception in method check: [{}]".format(str(e)))

        # Method OK, but type wrong, so exception expected
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_method_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'method_name': "method_one_param",
                             'expected_param_types': [float],
                             'exception_on_error': True}
                          )

    def test_method_multi_param(self):
        # Method & correct Types present so no exception expected
        #
        try:
            Reflection.check_method_exists(self.test_obj, "method_two_param", [int, Dict])
        except Exception as e:
            self.fail("Unexpected Exception in method check: [{}]".format(str(e)))

        # Method OK, but type wrong, so exception expected
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_method_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'method_name': "method_two_param",
                             'expected_param_types': [float, Dict],
                             'exception_on_error': True}
                          )

    def test_simple_property(self):
        # Property exists and type as expected so no exception
        #
        try:
            Reflection.check_property_exists(self.test_obj, "name", str)
        except Exception as e:
            self.fail("Unexpected Exception in method check: [{}]".format(str(e)))

        # Property missing so exception expected
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_property_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'property_name': "property_not_in_class",
                             'expected_property_type': str,
                             'exception_on_error': True}
                          )

        # Property present but type wrong so exception expected
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_property_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'property_name': "name",
                             'expected_property_type': int,
                             'exception_on_error': True}
                          )

    def test_method_class_param(self):
        # Method & Type exist so no exception expected
        #
        try:
            Reflection.check_method_exists(self.test_obj, "method_class_param", [DummyClass])
        except Exception as e:
            self.fail("Unexpected Exception in method check: [{}]".format(str(e)))

        # Method present but type wrong
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_method_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'method_name': "method_class_param",
                             'expected_param_types': [DummyClass2],
                             'exception_on_error': True}
                          )

    def test_class_method(self):
        # Method & Type exist so no exception expected
        #
        try:
            Reflection.check_method_exists(self.test_obj, "class_method", [Tuple[int, int], Dict])
        except Exception as e:
            self.fail("Unexpected Exception in method check: [{}]".format(str(e)))

        # Method present but type wrong
        #
        self.assertRaises(NotImplementedError,
                          Reflection.check_method_exists,
                          **{'object_to_reflect_on': self.test_obj,
                             'method_name': "class_method",
                             'expected_param_types': [Tuple[float, int], Dict],
                             'exception_on_error': True}
                          )


if __name__ == "__main__":
    unittest.main()
