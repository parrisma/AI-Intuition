from typing import Dict
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.webstream import WebStream
from journey11.src.lib.settings import Settings
from journey11.src.lib.elastic.esutil import ESUtil
from journey11.src.test.run_spec.runspec import RunSpec
from journey11.src.lib.aitrace.trace import Trace


class ElasticEnvBuilder(EnvBuilder):

    def execute(self,
                context: Dict) -> None:
        """
        Execute actions to establish the elastic environment.
        Get the environment specific settings for elastic host and port, open a connection and save into the bootstrap
        context

        :param context: Dictionary of current environment context that can be used or added to by builder
        :return: None: Implementation should throw and exception to indicate failure
        """
        """
        Get the environment specific settings for elastic host and port, open a connection and save
        into the bootstrap context
        """
        Trace.log().info("Invoked : {}".format(str(self)))
        Trace.log().info("Initiating Elastic logging capability for trace")
        settings = Settings(settings_yaml_stream=WebStream(RunSpec.elastic_settings_yaml()),
                            bespoke_transforms=RunSpec.setting_transformers())
        hostname, port_id = settings.default()
        context[EnvBuilder.ElasticDbConnectionContext] = ESUtil.get_connection(hostname=hostname,
                                                                               port_id=port_id)
        Trace.log().info("Trace Elastic logging capability enabled")
        return

    def uuid(self) -> str:
        """
        The immutable UUID of this build phase. This should be fixed at the time of coding as it is
        used in the environment factory settings to sequence build stages
        :return: immutable UUID
        """
        return "55cd885be0004c6d84857c9cd260e417"

    def __str__(self) -> str:
        return "Elastic Environment Builder - Id: {}".format(self.uuid())

    def __repr__(self):
        return self.__str__()
