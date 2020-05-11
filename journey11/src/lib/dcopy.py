import re
from typing import List, Dict
from enum import Enum
from copy import deepcopy


class _Dcopyf:
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


class Dcopy:
    _copy_map = {type(list()).__name__: _Dcopyf.copy_list,
                 type(dict()).__name__: _Dcopyf.copy_dict}

    @staticmethod
    def deep_corresponding_copy(src, tgt):
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
        if isinstance(src, (int, float, type(None), str, bool, Enum)):
            if not isinstance(src, type(tgt)):
                raise TypeError("Source and Target are not of same type {} <> {}".format(type(src), type(tgt)))
            result = src
        elif type(src).__name__ in Dcopy._copy_map:
            if not isinstance(src, type(tgt)):
                raise TypeError("Source and Target are not of same type {} <> {}".format(type(src), type(tgt)))
            result = Dcopy._copy_map[type(src).__name__](src, tgt)
        else:
            result = tgt
            v_tgt = dict([(x, getattr(tgt, x)) for x in dir(tgt) if
                          not callable(getattr(tgt, x)) and re.search("^__.*__$", x) is None])

            v_src = dict([(x, getattr(src, x)) for x in dir(src) if
                          not callable(getattr(src, x)) and re.search("^__.*__$", x) is None])
            for vsk, vsv in v_src.items():
                if vsk in v_tgt:
                    print("{} - {}".format(str(vsk), str(vsv)))
                    setattr(tgt, vsk, Dcopy.deep_corresponding_copy(vsv, v_tgt[vsk]))
                    print(str(v_tgt[vsk]))
        return result
