from abc import ABC, abstractmethod
import re
from typing import List, Dict, get_type_hints
from pydoc import locate
from enum import Enum
from copy import deepcopy


class _DcopyCore(ABC):
    _handlers = list()

    SRC_ANNOTATION_ARG = 'src_annotation'
    TGT_ANNOTATION_ARG = 'tgt_annotation'

    @staticmethod
    def get_handlers() -> List['_DcopyCore']:
        return _DcopyCore._handlers

    @staticmethod
    def register_handler(handler: '_DcopyCore') -> None:
        """
        Add a DCopy handler to the known set of handler. These handlers will have their register methods invoked
        when DCopy initialized.
        :param handler: The handler to register
        """
        _DcopyCore._handlers.append(handler)
        return

    @staticmethod
    @abstractmethod
    def register_copy_maps(copy_map: Dict) -> Dict:
        """
        Register capabilities to map (copy) from Type to Type
        :param copy_map: The current map
        :return: the map with (optional) additional map functions in
        """
        pass

    @staticmethod
    @abstractmethod
    def register_collection(collection_map: Dict) -> Dict:
        """
        Register types that should be treated as iterable collections
        :param collection_map: The current collection map
        :return: the map with (optional) additional collections in
        """
        pass

    @staticmethod
    @abstractmethod
    def register_reference_type(ref_map: Dict) -> Dict:
        """
        Register types that are copy in place and do not need assignment after deep copy.
        :param ref_map: The current ref map
        :return: the map with (optional) additional ref types in
        """
        pass

    @staticmethod
    def tname(t) -> str:
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
        return "{}:{}".format(_DcopyCore.tname(t_from), _DcopyCore.tname(t_to))

    @staticmethod
    def new_from_annotation(annotation_type: str, **kwargs):
        """
        Locate the annotation type and return a new object of that type. This assumes object has default
        (parameter less constrictor).

        -param- **kwargs: expect key annotation= to be passed as string
        :return: A new object matching the type of the annotation

        TODO: Find out how to extract type of the list element from the List annotation directly.
        """
        annotation = str(kwargs.get(annotation_type, None))
        t = None
        if annotation != "None":
            if re.search("^typing.List.*]$", annotation):  # Yuk
                annotation = annotation[12: -1]
            try:
                t = locate(annotation)()
            except Exception:
                t = None
        if t is None:
            raise TypeError("Failed to instantiate type from annotation {}".format(str(annotation)))
        return t


class _DcopyCollection(_DcopyCore):
    """
    Methods to handle deep copy of collections
    """

    LIST_TYPE = type(list())
    DICT_TYPE = type(dict())

    @staticmethod
    def copy_list(src: List,
                  tgt: List,
                  **kwargs) -> List:
        """
        Where there are corresponding list[i] update Target with Source
        Where Source is longer than Target append Source elements to Target elements
        :param src: Source list
        :param tgt: Target list to merge / update
        :return: Updated Target
        """
        n = min(len(src), len(tgt))
        for i in range(n):
            tgt[i] = Copy.deep_corresponding_copy(src[i], tgt[i])
        if len(src) > n:
            for i in range(n, len(src)):
                tgt.append(deepcopy(src[i]))
        return tgt

    @staticmethod
    def copy_dict(src: Dict,
                  tgt: Dict,
                  **kwargs) -> Dict:
        """
        Update the Target where keys overlap with source or insert where they are missing
        :param src: Source Dictionary
        :param tgt: Target Dictionary
        :return:
        """
        for k, v in src.items():
            if k in tgt:
                tgt[k] = Copy.deep_corresponding_copy(src[k], tgt[k])
            else:
                tgt[k] = deepcopy(src[k])
        return tgt

    @staticmethod
    def register_copy_maps(copy_map: Dict) -> Dict:
        """
        Register capabilities to map (copy) from Type to Type
        :param copy_map:
        :return:
        """
        copy_map[_DcopyCore.key(_DcopyCollection.LIST_TYPE, _DcopyCollection.LIST_TYPE)] = _DcopyCollection.copy_list
        copy_map[_DcopyCore.key(_DcopyCollection.DICT_TYPE, _DcopyCollection.DICT_TYPE)] = _DcopyCollection.copy_dict
        return copy_map

    @staticmethod
    def register_collection(collection_map: Dict) -> Dict:
        """
        Register types that should be treated as iterable collections
        :param collection_map: The current collection map
        :return: the map with (optional) additional collections in
        """
        collection_map[_DcopyCollection.LIST_TYPE.__name__] = True
        collection_map[_DcopyCollection.DICT_TYPE.__name__] = True
        return collection_map

    @staticmethod
    def register_reference_type(ref_map: Dict) -> Dict:
        """
        Register types that are copy in place and do not need assignment after deep copy.
        :param ref_map: The current ref map
        :return: the map with (optional) additional ref types in
        """
        return ref_map  # No ref types


class _DcopyEnum(_DcopyCore):

    @staticmethod
    def copy_enum_to_value(src: Enum,
                           tgt: object,
                           **kwargs) -> object:
        """
        Convert Enum to integer equiv - assumes integer values between src/tgt are the same.
        :param src: Enum to convert
        :param tgt: Value target (int, str etc)
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

    @staticmethod
    def copy_value_to_enum(src: object,
                           tgt: Enum,
                           **kwargs) -> Enum:
        """
        Convert value to Enum, assumes the Enum can be constructed from the given src object type
        :param src: value type (int, src etc)
        :param tgt: Enum to convert to.
        :return: The Enum target
        Note: We don't use isinstance() in the value type check as we want to be explicit and for example
        bool is instance of int and we dont want to allow translation of int value Enum to bool.
        """
        try:
            tgt = type(tgt)(src)
        except Exception as e:
            raise TypeError(
                "Cannot construct Enum type {} from .value type {} with error {}".format(type(tgt), type(src), str(e)))
        return tgt

    @staticmethod
    def register_copy_maps(copy_map: Dict) -> Dict:
        """
        Register capabilities to map (copy) from Type to Type.
        Note: Nothing is registered for Enum as they are called directly in the copy function not indirectly
        via the map.
        :param copy_map:
        :return: Updated copy_map
        """
        return copy_map

    @staticmethod
    def register_collection(collection_map: Dict) -> Dict:
        """
        Regsiter nothing as Enum is no a collection
        :param collection_map: The current collection map
        :return: the map with (optional) additional collections in
        """
        return collection_map

    @staticmethod
    def register_reference_type(ref_map: Dict) -> Dict:
        """
        Register types that are copy in place and do not need assignment after deep copy.
        :param ref_map: The current ref map
        :return: the map with (optional) additional ref types in
        """
        return ref_map  # No ref types


class _DcopyProto(_DcopyCore):

    @staticmethod
    def copy_list_2_protobuf_composite_repeat(src: List,
                                              tgt,
                                              **kwargs) -> object:
        """
        Where there are corresponding list[i] update Target with Source
        Where Source is longer than Target append Source elements to Target elements
        :param src: Source list
        :param tgt: Protobuf Composeite Repeat to merge to.
        :return: Updated Target
        """
        n = min(len(src), len(tgt))
        for i in range(n):
            tgt[i] = Copy.deep_corresponding_copy(src[i], tgt[i])
        if len(src) > n:
            for i in range(n, len(src)):
                _ = tgt.add()  # Extend the Protobuf repeat
                _ = Copy.deep_corresponding_copy(src[i], tgt[i])  # Direct update via reference
        return tgt

    @staticmethod
    def copy_list_2_protobuf_scalar_repeat(src: List,
                                           tgt,
                                           **kwargs) -> object:
        """
        Where there are corresponding list[i] update Target with Source
        Where Source is longer than Target append Source elements to Target elements
        :param src: Source list
        :param tgt: Protobuf Scalar Repeat to merge to.
        :return: Updated Target
        """
        n = min(len(src), len(tgt))
        for i in range(n):
            tgt[i] = Copy.deep_corresponding_copy(src[i], tgt[i])
        if len(src) > n:
            for i in range(n, len(src)):
                tgt.append(_DcopyCore.new_from_annotation(_DcopyCore.SRC_ANNOTATION_ARG, **kwargs))
                tgt[i] = Copy.deep_corresponding_copy(src[i], tgt[i])  # Direct update via reference
        return tgt

    @staticmethod
    def copy_protobuf_repeat_2_list(src,
                                    tgt: List,
                                    **kwargs) -> List:
        """
        Translate a protobuf-repeat into a List
        Where there are corresponding list[i] update Target with Source
        Where Source is longer than Target append Source elements to Target elements
        :param src: Source Protobuf repeat
        :param tgt: Target list to merge / update
        :return: Updated Target
        """
        n = min(len(src), len(tgt))
        for i in range(n):
            tgt[i] = Copy.deep_corresponding_copy(src[i], tgt[i])
        if len(src) > n:
            for i in range(n, len(src)):
                tgt.append(_DcopyCore.new_from_annotation(_DcopyCore.TGT_ANNOTATION_ARG, **kwargs))
                tgt[i] = Copy.deep_corresponding_copy(src[i], tgt[i])
        return tgt

    @staticmethod
    def register_copy_maps(copy_map: Dict) -> Dict:
        """
        Register capabilities to map (copy) from Type to Type.
        :param copy_map:
        :return: Updated copy_map
        """
        copy_map[_DcopyCore.key("RepeatedCompositeFieldContainer",
                                _DcopyCollection.LIST_TYPE)] = _DcopyProto.copy_protobuf_repeat_2_list
        copy_map[_DcopyCore.key(_DcopyCollection.LIST_TYPE,
                                "RepeatedCompositeFieldContainer")] = _DcopyProto.copy_list_2_protobuf_composite_repeat
        copy_map[_DcopyCore.key("RepeatedScalarFieldContainer",
                                _DcopyCollection.LIST_TYPE)] = _DcopyProto.copy_protobuf_repeat_2_list
        copy_map[_DcopyCore.key(_DcopyCollection.LIST_TYPE,
                                "RepeatedScalarFieldContainer")] = _DcopyProto.copy_list_2_protobuf_scalar_repeat

        return copy_map

    @staticmethod
    def register_collection(collection_map: Dict) -> Dict:
        """
        Register types that should be treated as iterable collections
        :param collection_map: The current collection map
        :return: the map with (optional) additional collections in
        """
        collection_map["RepeatedCompositeFieldContainer"] = True
        collection_map["RepeatedScalarFieldContainer"] = True
        return collection_map

    @staticmethod
    def register_reference_type(ref_map: Dict) -> Dict:
        """
        Register types that are copy in place and do not need assignment after deep copy.
        :param ref_map: The current ref map
        :return: the map with (optional) additional ref types in
        """
        ref_map["RepeatedCompositeFieldContainer"] = True
        ref_map["RepeatedScalarFieldContainer"] = True
        return ref_map


class Copy:
    _collection = dict()
    _ref_type = {}
    _copy_map = dict()

    @staticmethod
    def bootstrap() -> None:
        """
        Called by module __init__ to bind all handler classes.
        :return:
        """
        for d in _DcopyCore.get_handlers():
            d.register_copy_maps(Copy._copy_map)
            d.register_collection(Copy._collection)
            d.register_reference_type(Copy._ref_type)
        return

    @staticmethod
    def get_annotations(obj) -> Dict:
        """
        If the given object has annotations return them else an empty dictionary
        :param obj: The object to extract annotations for (if it has them)
        :return: Annotations as dictionary
        """
        annotations = None
        try:
            annotations = get_type_hints(obj)
        except Exception as _:
            annotations = dict()
        return annotations

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

        if names_to_prune is None:
            names_to_prune = list()

        if not isinstance(names_to_prune, list):
            names_to_prune = [names_to_prune]

        for name in names_to_prune:
            if name is not None:
                if not isinstance(name, str):
                    raise TypeError("Names to prune must be strings but given {}".format(type(name).__name__))
                if name in member_names:
                    del member_names[name]
        return member_names

    @staticmethod
    def member_annotations(member_name: str,
                           src_annotations: Dict,
                           tgt_annotations: Dict) -> Dict:
        """
        If there are any corresponding annotations to the member name return them in the src/tgt
        annotations dictionary
        :param member_name: The name of the member to chgeck for
        :param src_annotations: Annotations for Src Object
        :param tgt_annotations: Annotations for Tgt Object
        :return: Dictionary with any corresponding src/tgt annotations.
        """
        annotation_kwargs = dict()

        annotation = src_annotations.get(member_name, None)
        if annotation is not None:
            annotation_kwargs[_DcopyCore.SRC_ANNOTATION_ARG] = annotation

        annotation = tgt_annotations.get(member_name, None)
        if annotation is not None:
            annotation_kwargs[_DcopyCore.TGT_ANNOTATION_ARG] = annotation

        return annotation_kwargs

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
        ToDo : consider change to allow mapping of private __ members.
        """
        result = None
        if type(src).__name__ in Copy._collection:
            if _DcopyCore.key(type(src), type(tgt)) in Copy._copy_map:
                result = Copy._copy_map[_DcopyCore.key(type(src), type(tgt))](src, tgt, **kwargs)
            elif not isinstance(src, type(tgt)):
                raise TypeError("Source and Target are not of same type {} <> {}".format(type(src), type(tgt)))
        elif issubclass(type(src), Enum):
            result = _DcopyEnum.copy_enum_to_value(src=src, tgt=tgt, **kwargs)
        elif issubclass(type(tgt), Enum):
            result = _DcopyEnum.copy_value_to_enum(src=src, tgt=tgt, **kwargs)
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

            v_src = Copy.prune(v_src, **kwargs)

            tgt_annotations = Copy.get_annotations(tgt)
            src_annotations = Copy.get_annotations(src)

            for vsk, vsv in v_src.items():
                print(vsk)
                if vsk in v_tgt:
                    kwargs = {**kwargs, **Copy.member_annotations(vsk, src_annotations, tgt_annotations)}
                    res = Copy.deep_corresponding_copy(vsv, v_tgt[vsk], **kwargs)
                    if type(res).__name__ not in Copy._ref_type:
                        setattr(tgt, vsk, res)
        return result
