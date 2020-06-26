from typing import Dict
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.aitrace.elastichandler import ElasticHandler
from journey11.src.lib.webstream import WebStream
from journey11.src.lib.settings import Settings
from journey11.src.lib.elastic.esutil import ESUtil
from journey11.src.test.run_spec.runspec import RunSpec


class TraceElasticEnvBuilder(EnvBuilder):

    def execute(self,
                context: Dict) -> None:
        """
        Execute actions to build the element of the environment owned by this builder
        :param context: Dictionary of current environment context that can be used or added to by builder
        :return: None: Implementation should throw and exception to indicate failure
        """
        Trace.log().info("Invoked : {}".format(str(self)))
        Trace.log().info("Establishing Trace connection for Elastic logging")
        es = context.get(EnvBuilder.ElasticDbConnectionContext, None)
        if es is None:
            raise ValueError("Elastic Connection not available in supplied context")
        settings = Settings(settings_yaml_stream=WebStream(RunSpec.trace_settings_yaml()),
                            bespoke_transforms=RunSpec.setting_transformers())
        elastic_index_name, elastic_index_json = settings.default()

        # Ensure Trace Log index is created in elastic db
        ESUtil.create_index_from_json(es=es,
                                      idx_name=elastic_index_name,
                                      json_stream=WebStream(elastic_index_json))

        # Link the Trace Logging to the elastic handler
        Trace.enable_elastic_handler(ElasticHandler(elastic_connection=es, log_index_name=elastic_index_name))

        Trace.log().info("Trace connected to Elastic")
        return

    def uuid(self) -> str:
        """
        The immutable UUID of this build phase. This should be fixed at the time of coding as it is
        used in the environment factory settings to sequence build stages
        :return: immutable UUID
        """
        return "672c73af91e942c1a5685545411d919b"

    def __str__(self) -> str:
        return "Trace Elastic Logging Builder - Id: {}".format(self.uuid())

    def __repr__(self):
        return self.__str__()
