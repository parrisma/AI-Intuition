from typing import Dict
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.aitrace.trace import Trace


class AITraceEnvBuilder(EnvBuilder):

    def execute(self,
                context: Dict) -> bool:
        """
        Execute actions to build the element of the environment owned by this builder
        :param context: Dictionary of current environment context that can be used or added to by builder
        :return: True if environment build should continue
        """
        es = context.get(EnvBuilder.ElasticDbConnectionContext, None)
        if es is None:
            raise ValueError("Elastic Connection not available in supplied context")
        Trace.enable_elastic_handler(es)
        return True

    def uuid(self) -> str:
        """
        The immutable UUID of this build phase. This should be fixed at the time of coding as it is
        used in the environment factory settings to sequence build stages
        :return: immutable UUID
        """
        return "672c73af-91e9-42c1-a568-5545411d919b"
