import re
from typing import List, Dict, Type, AnyStr
from enum import Enum
from copy import deepcopy


class _Dcopyf:
    LIST_TYPE = type(list())
    DICT_TYPE = type(dict())

    @staticmethod
    def _tname(t) -> str:
        """
        Return the name of the type t or return t is t is as string on assumption it is a type name already
        :param t: Type or name of type as string
        :return: Type name as string
        """
        if isinstance(t, type):
            tn = t.__name__
        elif isinstance(t, str):
            tn = t
        else:
            raise TypeError("from type must be a Type or a Type name - given {}".format(type(t)))
        return tn

    @staticmethod
    def key(t_from,
            t_to) -> str:
        """
        Return look-up key for Type to Type mapping function
        :param t_from: Type to map from
        :param t_to: Type to map to
        :return: Mapping Key
        """
        return "{}:{}".format(_Dcopyf._tname(t_from), _Dcopyf._tname(t_to))

    @staticmethod
    def copy_list(src: List, tgt: List) -> List:
        """
        Where there are corresponding list[i] update Target with Source
        Where Source is longer than Target append Source elements to Target elements
        :param src: Source list
        :param tgt: Target list to merge / update
        :return: Updated Target
        """
        n = min(len(src), len(tgt))
        for i in range(n):
            tgt[i] = Dcopy.deep_corresponding_copy(src[i], tgt[i])
        if len(src) > n:
            for i in range(n, len(src)):
                tgt.append(deepcopy(src[i]))
        return tgt

    @staticmethod
    def copy_list_2_protobuf_repeat(src: List, tgt: object) -> object:
        """
        Where there are corresponding list[i] update Target with Source
        Where Source is longer than Target append Source elements to Target elements
        :param src: Source list
        :param tgt: Target list to merge / update
        :return: Updated Target
        """
        n = min(len(src), len(tgt))
        for i in range(n):
            tgt[i] = Dcopy.deep_corresponding_copy(src[i], tgt[i])
        if len(src) > n:
            for i in range(n, len(src)):
                nw = tgt.add()
                nw = Dcopy.deep_corresponding_copy(src[i], tgt[i])
        return tgt

    @staticmethod
    def copy_dict(src: Dict, tgt: Dict) -> Dict:
        """
        Update the Target where keys overlap with source or insert where they are missing
        :param src: Source Dictionary
        :param tgt: Target Dictionary
        :return:
        """
        for k, v in src.items():
            if k in tgt:
                tgt[k] = Dcopy.deep_corresponding_copy(src[k], tgt[k])
            else:
                tgt[k] = deepcopy(src[k])
        return tgt

    @staticmethod
    def copy_enum(src: Enum, tgt: object) -> object:
        """
        Convert Enum to integer equiv - assumes integer values between src/tgt are the same.
        :param src: Enum to convert
        :param tgt: Integer target in Protobuf
        :return: The updated target object
        Note: We don't use isinstance() in the value type check as we want to be explicit and for example
        bool is instance of int and we dont want to allow translation of int value Enum to bool.
        """
        if isinstance(tgt, Enum):
            tgt = src
        elif type(tgt) == type(src.value):  # We don't use isinstance() by design
            tgt = src.value
        else:
            raise TypeError("Cannot copy type {} to Enum with .value type {}".format(type(tgt), type(src.value)))
        return tgt


class Dcopy:
    _collection = {_Dcopyf.LIST_TYPE.__name__: True,
                   _Dcopyf.DICT_TYPE.__name__: True}
    _ref_type = {"RepeatedCompositeFieldContainer": True}
    _copy_map = {_Dcopyf.key(_Dcopyf.LIST_TYPE, _Dcopyf.LIST_TYPE): _Dcopyf.copy_list,
                 _Dcopyf.key(_Dcopyf.DICT_TYPE, _Dcopyf.DICT_TYPE): _Dcopyf.copy_dict,
                 _Dcopyf.key(_Dcopyf.LIST_TYPE, "RepeatedCompositeFieldContainer"): _Dcopyf.copy_list_2_protobuf_repeat}

    @staticmethod
    def prune(member_names: Dict,
              **kwargs) -> Dict:
        """
        Remove special member names if passed as kwrgs param.
        :param member_names: Current list of member names
        :param kwargs: Look for 'prune' :parameter optionally passed
        :return: member names with any prune names removed.
        """
        names_to_prune = kwargs.get('prune', list())
        for name in names_to_prune:
            if name in member_names:
                del member_names[name]
        return member_names

    @staticmethod
    def deep_corresponding_copy(src,
                                tgt,
                                **kwargs):
        """
        Iterate all member variables of target and where there are corresponding member variables update target
        with source.
        Where there are collections update the collection where there is overlap and insert/append where there are
        elements in source not in target
        When Target is updated the target must be the same type as the Source. This event applies in the heterogeneous
        collections, items that corresponding wil throw and error if they are not of the same type.
        :param src: The source object
        :param tgt: The target object to be updated with corresponding source memebers
        :return: The updated version of Target.
        ToDo : consider change to allow mapping of private members.
        """
        result = None
        if type(src).__name__ in Dcopy._collection:
            if _Dcopyf.key(type(src), type(tgt)) in Dcopy._copy_map:
                result = Dcopy._copy_map[_Dcopyf.key(type(src), type(tgt))](src, tgt)
            elif not isinstance(src, type(tgt)):
                raise TypeError("Source and Target are not of same type {} <> {}".format(type(src), type(tgt)))
        elif issubclass(type(src), Enum):
            result = _Dcopyf.copy_enum(src=src, tgt=tgt)
        elif isinstance(src, (int, float, type(None), str, bool)):
            if not isinstance(src, type(tgt)):
                raise TypeError("Source and Target are not of same type {} <> {}".format(type(src), type(tgt)))
            result = src
        else:
            result = tgt
            v_tgt = dict([(x, getattr(tgt, x)) for x in dir(tgt) if
                          not callable(getattr(tgt, x)) and re.search("^__.*__$", x) is None])

            v_src = dict([(x, getattr(src, x)) for x in dir(src) if
                          not callable(getattr(src, x)) and re.search("^__.*__$", x) is None])

            v_src = Dcopy.prune(v_src, **kwargs)

            for vsk, vsv in v_src.items():
                print(vsk)
                if vsk in v_tgt:
                    res = Dcopy.deep_corresponding_copy(vsv, v_tgt[vsk])
                    if type(res).__name__ not in Dcopy._ref_type:
                        setattr(tgt, vsk, res)
        return result
