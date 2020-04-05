from typing import Dict, Type, List
import logging
import inspect


class Reflection:
    no_params = [type(None)]

    @classmethod
    def check_method_exists(cls,
                            object_to_reflect_on,
                            method_name: str,
                            expected_param_types: List[Type],
                            exception_on_error: bool = True) -> bool:

        if not isinstance(expected_param_types, list):
            raise ValueError("expected_param_type should be of form List[Type]")

        methods = cls._get_obj_methods(object_to_reflect_on)
        if method_name in methods:
            params = inspect.signature(methods[method_name]).parameters
            if expected_param_types == Reflection.no_params:
                if len(params) == 0:
                    return True
            else:
                actual_param_types = [p.annotation for p in list(params.values())]
                if len(actual_param_types) == len(expected_param_types):
                    params_match = True if False not in [v for v in [e == a for (e, a) in zip(expected_param_types,
                                                                                              actual_param_types)]] \
                        else False
                    if params_match:
                        return True

        if exception_on_error:
            msg = "Must Implement method {}(".format(method_name)
            if expected_param_types == Reflection.no_params:
                msg = "{})".format(msg)
            else:
                pn = 1
                for pt in expected_param_types:
                    msg = "{}p{}:{},".format(msg, pn, Reflection._name(pt))
                    pn += 1
                msg = "{})".format(msg[:-1])
            logging.critical(msg=msg)
            raise NotImplementedError(msg)

        return False

    @classmethod
    def check_property_exists(cls,
                              object_to_reflect_on,
                              property_name: str,
                              expected_property_type: Type,
                              exception_on_error: bool = True) -> bool:
        if not isinstance(expected_property_type, type):
            raise ValueError("expected_param_type should be a type")

        properties = cls._get_obj_properties(object_to_reflect_on)
        if property_name in properties and type(properties[property_name]) == expected_property_type:
            return True

        if exception_on_error:
            msg = "Must Implement method {}(p1:{})".format(property_name, Reflection._name(expected_property_type))
            logging.critical(msg=msg)
            raise NotImplementedError(msg)

        return False

    @classmethod
    def _get_obj_methods(cls, obj) -> Dict:
        return dict(inspect.getmembers(obj, inspect.ismethod))

    @classmethod
    def _get_obj_properties(cls, obj) -> Dict:
        return dict(inspect.getmembers(obj, lambda o: not callable(o)))

    @classmethod
    def _name(cls, o: object):
        n = None
        try:
            n = o.__name__
        except:
            try:
                n = o._name
            except:
                n = "<?>"
        return n
