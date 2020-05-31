import sys
import yaml
from typing import Dict, List, Type
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
    _item_name = 0
    _item_protobuf = 1
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
        self._map_type_to_uuid = dict()
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
            protobuf_type = self.get_protobuf_type(item_protobuf)
            if protobuf_type is None:
                raise ImportError("protobuf object type {} cannot be found in any loaded module".format(item_protobuf))
            self._map_uuid_to_type[item_uuid] = [item_name, protobuf_type]
            self._map_type_to_uuid[str(protobuf_type)] = [item_name, item_uuid]
        return

    def get_uuid_by_type(self,
                         protobuf_type: Type) -> str:
        """
        Get the UUID that maps to the given protobuf type
        :param protobuf_type: The Protobif type to get the mapped UUID for
        :return: UUID mapped to the protobuf type or None if no mapping
        """
        type_uuid = None
        if str(protobuf_type) in self._map_type_to_uuid:
            type_uuid = self._map_type_to_uuid[str(protobuf_type)][MessageTypeMap._item_uuid]
        return type_uuid

    def get_type_by_uuid(self,
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

    def get_protobuf_type(self,
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
