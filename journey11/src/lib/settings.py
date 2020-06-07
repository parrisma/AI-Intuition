import yaml
import socket
from typing import Dict, List, Type, Tuple
from datetime import datetime


class Settings:
    _header = "header"
    _version_tag = 'version'
    _date_tag = 'date'
    _description_tag = 'description'
    _header_items = [[_version_tag, '_version'],
                     [_date_tag, '_date'],
                     [_description_tag, '_description']]

    _kafka = "kafka"
    _host_tag = 'host'
    _port_tag = 'port'
    _msg_map_url_tag = 'msg_map_url'
    _kafka_items = [[_host_tag, '_host'],
                    [_port_tag, '_port'],
                    [_msg_map_url_tag, '_msg_map_url']]
    _curr_host_marker = "<current-host>"

    def __init__(self,
                 settings_yaml_stream):
        """
        Boot strap the settings form the supplied YAML stream
        :param settings_yaml_stream: A callable that returns an open stream to the YAML source
        """
        if not hasattr(settings_yaml_stream, "__call__"):
            raise ValueError(
                "YAML stream sources must be callable, [{}} is not callable".format(type(settings_yaml_stream)))

        # Header
        self._version = None
        self._date = None
        self._description = None

        # Kafka
        self._host = None
        self._port = None
        self._msg_map_url = None

        self._yaml_stream = settings_yaml_stream
        self._load_settings()
        return

    @property
    def description(self) -> str:
        return self._description

    @property
    def version(self) -> str:
        return self._version

    @property
    def date(self) -> datetime:
        return datetime.strptime(self._date, "%d %b %Y")

    @property
    def kafka(self) -> Tuple[str, str, str]:
        return self._host, self._port, self._msg_map_url

    def _load_settings(self) -> None:
        """
        Load the settings from YAML config.
        """
        src = self._yaml_stream()
        yml_map = yaml.safe_load(src)
        self._parse_header(yml_map.get(Settings._header))
        self._parse_kafka(yml_map.get(Settings._kafka))
        src.close()
        return

    def _parse_header(self,
                      header: Dict) -> None:
        """
        Extract the header details from the header section of the yaml
        :param header: The header section of the as loaded from the YAML source
        """
        for item in Settings._header_items:
            if item[0] not in header:
                raise ValueError("Mal-structured type map yaml [{}] is missing from header".format(item[0]))
            setattr(self, item[1], header[item[0]])
        return

    def _parse_kafka(self,
                     kafka: Dict) -> None:
        """
        Extract the header details from the header section of the yaml
        :param kafka: The kafka section of the as loaded from the YAML source
        """
        for item in Settings._kafka_items:
            if item[0] not in kafka:
                raise ValueError("Mal-structured type map yaml [{}] is missing from kafka".format(item[0]))
            setattr(self, item[1], kafka[item[0]])
        if self._host == Settings._curr_host_marker:
            self._host = socket.gethostbyname(socket.gethostname())
        return
