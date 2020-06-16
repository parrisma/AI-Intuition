from journey11.src.lib.kpubsub.kpubsub import KPubSub
from journey11.src.lib.webstream import WebStream
from journey11.src.lib.settings import Settings
from journey11.src.test.build_spec.runspec import RunSpec


class SimpleKps:
    def __init__(self):
        """
        Bootstrap a Kafka Pub Sub Object by picking up the default run spec. This relies on system
        environment variable used by RunSpec module __inti__ to pick up the YAML settings file.

        This assumes a Kafka service is up and running at the advertised host/port.
        """
        settings = Settings(settings_yaml_stream=WebStream(RunSpec.pubsub_settings_yaml()),
                            bespoke_transforms=RunSpec.setting_transformers())
        hostname, port_id, msg_map_url = settings.default()
        self._kps = KPubSub(server=hostname,
                            port=port_id,
                            yaml_stream=WebStream(msg_map_url))
        return

    @property
    def connection(self) -> KPubSub:
        """
        The Kafka Pub Sub connection established during class __init__
        :return: Kakfa Pub Sub (KPubSub) connection
        """
        return self._kps
