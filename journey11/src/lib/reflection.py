from typing import Dict
import logging
import inspect


class Reflection:

    @classmethod
    def check_method_exists(cls,
                            object_to_reflect_on,
                            method_name: str) -> None:
        msg = "Must Implement method {}(arg1)".format(method_name)
        methods = cls._get_obj_methods(object_to_reflect_on)
        if method_name not in methods:
            logging.critical(msg=msg)
            raise NotImplementedError(msg)

    @classmethod
    def check_property_exists(cls,
                              object_to_reflect_on,
                              property_name: str) -> None:
        msg = "Must Implement method {}(arg1)".format(property_name)
        properties = cls._get_obj_properties(object_to_reflect_on)
        if property_name not in properties:
            logging.critical(msg=msg)
            raise NotImplementedError(msg)

    @classmethod
    def _get_obj_methods(cls, obj) -> Dict:
        return dict(inspect.getmembers(obj, inspect.ismethod))

    @classmethod
    def _get_obj_properties(cls, obj) -> Dict:
        return dict(inspect.getmembers(obj, lambda o: not callable(o)))
