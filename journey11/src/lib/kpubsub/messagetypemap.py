import sys
import yaml
from typing import Dict, List, Type, Tuple
from datetime import datetime


class MessageTypeMap:
    _header = "header"
    _header_items = [['version', '_map_version'],
                     ['date', '_map_date'],
                     ['description', '_map_description']]
    _message_map = "message_map"
    _message_item = "message"
    _map_item_name = "name"
    _map_item_uuid = "uuid"
    _map_item_protobuf = "protobuf"
    _map_item_native = "native"
    _item_name = 0
    _item_protobuf = 1
    _item_native = 2
    _item_uuid = 1

    def __init__(self,
                 map_yaml_stream):
        """
        Boot strap the map form the supplied YAML stream
        :param map_yaml_stream: A callable that returns an open stream to the YAML source
        """
        if not hasattr(map_yaml_stream, "__call__"):
            raise ValueError("YAML stream sources must be callable, [{}} is not callable".format(type(map_yaml_stream)))

        self._protobuf_types = dict()
        self._yaml_stream = map_yaml_stream
        self._logical_map = dict()
        self._implementation_map = dict()
        self._map_source = str()
        self._map_version = str()
        self._map_date = str()
        self._map_description = str()
        self._map_protobuf_type_to_uuid = dict()
        self._map_native_type_to_uuid = dict()
        self._map_uuid_to_type = dict()
        self._load_map()
        return

    @property
    def description(self) -> str:
        return self._map_description

    @property
    def version(self) -> str:
        return self._map_version

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._map_date, "%d %b %Y")

    def _load_map(self) -> None:
        """
        Load the message map from YAML config.
        todo: support load from WEB URL
        """
        src = self._yaml_stream()
        yml_map = yaml.safe_load(src)
        self._parse_header(yml_map.get(MessageTypeMap._header))
        self._parse_map(yml_map.get(MessageTypeMap._message_map))
        src.close()
        return

    def _parse_header(self,
                      header: Dict) -> None:
        """
        Extract the header details from the header section of the yaml
        :param header: The header section of the as loaded from the YAML source
        """
        for item in MessageTypeMap._header_items:
            if item[0] not in header:
                raise ValueError("Mal-structured type map yaml [{}] is missing from header".format(item[0]))
            setattr(self, item[1], header[item[0]])
        return

    def _parse_map(self,
                   message_map: List) -> None:
        """
        Iterate over all map entries and load into the internal dictionary
        :param message_map: The list of message map entries
        """
        for map_item in message_map:
            item_name = map_item[MessageTypeMap._message_item][MessageTypeMap._map_item_name]
            item_uuid = map_item[MessageTypeMap._message_item][MessageTypeMap._map_item_uuid]
            item_protobuf = map_item[MessageTypeMap._message_item][MessageTypeMap._map_item_protobuf]
            protobuf_type = self._get_type_by_name(item_protobuf)
            item_native = map_item[MessageTypeMap._message_item][MessageTypeMap._map_item_native]
            native_type = self._get_type_by_name(item_native)
            if protobuf_type is None:
                raise ImportError("protobuf object type {} cannot be found in any loaded module".format(item_protobuf))
            self._map_uuid_to_type[item_uuid] = [item_name, protobuf_type, native_type]
            self._map_protobuf_type_to_uuid[str(protobuf_type)] = [item_name, item_uuid]
            self._map_native_type_to_uuid[str(native_type)] = [item_name, item_uuid]
        return

    def get_uuid_by_type(self,
                         object_type: Type) -> str:
        """
        Get the UUID that maps to the given protobuf type
        :param object_type: The Native or Protobuf type to get the mapped UUID for
        :return: UUID mapped to the native or protobuf type or None if no mapping
        """
        type_uuid = None
        if str(object_type) in self._map_protobuf_type_to_uuid:
            type_uuid = self._map_protobuf_type_to_uuid[str(object_type)][MessageTypeMap._item_uuid]
        if type_uuid is None and str(object_type) in self._map_native_type_to_uuid:
            type_uuid = self._map_native_type_to_uuid[str(object_type)][MessageTypeMap._item_uuid]
        return type_uuid

    def get_protobuf_type_by_uuid(self,
                                  uuid: str) -> Type:
        """
        Get the protobuf object name that maps to the given UUID
        :param uuid: The UUID of the protobuf object
        :return: The Protobuf Object or None if mapping not found
        """
        protobuf = None
        if uuid in self._map_uuid_to_type:
            protobuf = self._map_uuid_to_type[uuid][MessageTypeMap._item_protobuf]
        return protobuf

    def get_native_type_by_uuid(self,
                                uuid: str) -> Type:
        """
        Get the native object name that maps to the given UUID
        :param uuid: The UUID of the native object
        :return: The native Object or None if mapping not found
        """
        protobuf = None
        if uuid in self._map_uuid_to_type:
            protobuf = self._map_uuid_to_type[uuid][MessageTypeMap._item_native]
        return protobuf

    def get_partner_object_type(self,
                                object_type: Type) -> Type:
        """
        Get the partner object type - if protobuf type get native partner else if native object get
        protobuf partner
        :param object_type: The type of object to get the partner for
        :return: The type of the partner object or None if does nto exist
        """
        partner_type = None
        obj_uuid = self.get_uuid_by_type(object_type=object_type)
        partner_type = self.get_native_type_by_uuid(obj_uuid)
        if partner_type is not None and partner_type == object_type:
            partner_type = self.get_protobuf_type_by_uuid(obj_uuid)
        else:
            partner_type = self.get_protobuf_type_by_uuid(obj_uuid)
            if partner_type is not None and partner_type == object_type:
                partner_type = self.get_native_type_by_uuid(obj_uuid)

        return partner_type

    def _get_type_by_name(self,
                          type_name) -> Type:
        """
        Return the Type object for the given type name
        :param type_name: The type name to find & create
        :return: The Type of the given type name
        """
        typ = self._protobuf_types.get(type_name, None)
        if typ is None:
            for module in sys.modules.keys():
                if type_name in dir(sys.modules[module]):
                    typ = getattr(sys.modules[module], type_name)
                    break
        return typ

    def native_to_protobuf(self) -> List[Tuple[Type, Type]]:
        """
        Return a list of type tuples that desribe all native to protobuf type mappings
        :return: List of Tuples of Native to Protobuf type or None
        """
        res = list()
        for v in self._map_uuid_to_type.values():
            res.append((v[2], v[1]))
        if len(res) == 0:
            res = None
        return res
