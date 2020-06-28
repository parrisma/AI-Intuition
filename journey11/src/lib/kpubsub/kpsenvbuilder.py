from typing import Dict
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.kpubsub.kpsutil import KPSUtil
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.webstream import WebStream
from journey11.src.lib.settings import Settings
from src.lib.envboot.runspec import RunSpec


class KPSEnvBuilder(EnvBuilder):
    _settings: Settings
    _context: Dict
    _run_spec: RunSpec
    _trace: Trace

    def __init__(self,
                 context: Dict):
        self._context = context
        self._trace = self._context[EnvBuilder.TraceContext]
        self._run_spec = self._context[EnvBuilder.RunSpecificationContext]
        return

    def execute(self,
                purge: bool) -> None:
        """
        Execute actions to establish the Kafka Environment

        Assumes the Elastic environment is already established.

        :param purge: If true eliminate any existing context and data
        :return: None: Implementation should throw and exception to indicate failure
        """
        """
        Get the environment specific settings for Kafka
        """
        self._trace.log().info("Invoked : {}".format(str(self)))
        self._trace.log().info("Initiating Kafka Environment")
        self._context[EnvBuilder.KafkaPubSubContext] = KPSUtil(**KPSUtil.args_from_run_spec(self._run_spec)).kps()
        self._trace.log().info("Kafka environment Initiated")
        return

    def uuid(self) -> str:
        """
        The immutable UUID of this build phase. This should be fixed at the time of coding as it is
        used in the environment factory settings to sequence build stages
        :return: immutable UUID
        """
        return "6fd443c3f05b4d01950921f912519960"

    def __str__(self) -> str:
        return "Kafka Environment Builder - Id: {}".format(self.uuid())

    def __repr__(self):
        return self.__str__()
