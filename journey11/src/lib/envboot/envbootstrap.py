from typing import Dict
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.namegen.namegen import NameGen
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.elastic.elasticenvbuilder import ElasticEnvBuilder
from journey11.src.lib.aitrace.traceelasticenvbuilder import TraceElasticEnvBuilder


class EnvBootstrap:
    # Annotation
    _name: str
    _env_id: str
    _context: Dict[str, object]

    _name = None
    _env_id = None
    _context = None

    @classmethod
    def __init__(cls,
                 name: str = None):
        if cls._context is None:
            cls._context = dict()
            cls._env_id = UniqueRef().ref
            if name is None or len(name) == 0:
                cls._name = NameGen.generate_random_name()

            Trace()  # Basic trace with just console logging.
            Trace.log().info("Starting {}".format(cls.__str__()))
            cls._bootstrap()
            Trace.log().info("Started {}".format(cls.__str__()))
        else:
            if name is not None:
                raise RuntimeError("Environment {} cannot be renamed".format(cls.__str__()))
        return

    @classmethod
    def _bootstrap(cls) -> None:
        """
        Execute the environment builders.
        Note: At the moment this is hard coded but will move to a YAML settings file.
        """
        ElasticEnvBuilder().execute(cls._context)
        TraceElasticEnvBuilder().execute(cls._context)
        return

    @classmethod
    def __str__(cls):
        return "Env: {} - Id: {}".format(cls._name, cls._env_id)

    @classmethod
    def __repr__(cls):
        return cls.__str__()
