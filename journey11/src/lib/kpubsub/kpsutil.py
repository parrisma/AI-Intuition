from typing import Callable, IO, Dict
from journey11.src.lib.kpubsub.kpubsub import KPubSub
from journey11.src.lib.kpubsub.messagetypemap import MessageTypeMap
from journey11.src.lib.webstream import WebStream
from journey11.src.lib.settings import Settings
from src.lib.envboot.runspec import RunSpec


class KPSUtil:
    # Annotation
    _kps: KPubSub
    _message_type_map: MessageTypeMap
    _hostname: str
    _port_id: str
    _yaml_stream: Callable[[], IO[str]]

    def __init__(self,
                 hostname: str,
                 port_id: str,
                 yaml_stream: Callable[[], IO[str]]):
        self._hostname = hostname
        self._port_id = port_id
        self._yaml_stream = yaml_stream
        self._message_type_map = None
        self._kps = None
        self._kps = self.kps()
        return

    def kps(self) -> KPubSub:
        """
        Return the KPubSub instance
        :return: the KPubSub instance.
        """
        # We expect a Kafka server running on the host defined in the settings yaml. This can be run up with the
        # Swarm service or stand along container script that is also part of this project.
        if self._kps is None:
            self._kps = KPubSub(server=self._hostname,
                                port=self._port_id,
                                yaml_stream=self._yaml_stream)
        return self._kps

    def message_type_map(self) -> MessageTypeMap:
        """
        Get the message type map
        :return: Message type map
        """
        if self._message_type_map is None:
            self._message_type_map = MessageTypeMap(self._yaml_stream)
        return self._message_type_map

    @staticmethod
    def args_from_run_spec(run_spec: RunSpec) -> Dict:
        settings = Settings(settings_yaml_stream=WebStream(run_spec.pubsub_settings_yaml()),
                            bespoke_transforms=run_spec.setting_transformers())
        host, port, yaml_url = settings.default()
        yaml_stream = WebStream(yaml_url)
        return {
            "hostname": host,
            "port_id": port,
            "yaml_stream": yaml_stream}
