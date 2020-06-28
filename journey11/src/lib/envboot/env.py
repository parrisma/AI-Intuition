from typing import Dict
from journey11.src.interface.envbuilder import EnvBuilder
from journey11.src.lib.uniqueref import UniqueRef
from journey11.src.lib.namegen.namegen import NameGen
from journey11.src.lib.aitrace.trace import Trace
from journey11.src.lib.aitrace.traceenvbuilder import TraceEnvBuilder
from journey11.src.lib.envboot.runspecenvbuilder import RunSpecEnvBuilder
from journey11.src.lib.elastic.elasticenvbuilder import ElasticEnvBuilder
from journey11.src.lib.aitrace.traceelasticenvbuilder import TraceElasticEnvBuilder
from journey11.src.lib.kpubsub.kpsenvbuilder import KPSEnvBuilder
from journey11.src.lib.kpubsub.kpubsub import KPubSub


class Env:
    # Annotation
    _name: str
    _env_id: str
    _context: Dict[str, object]
    _trace: Trace

    _name = None
    _env_id = None
    _context = None
    _trace = None  # Can only log via trace once the Trace Env Builder has run.

    @classmethod
    def __init__(cls,
                 purge: bool = False,
                 name: str = None):
        if cls._context is None:
            cls._context = dict()
            cls._env_id = UniqueRef().ref
            cls._context[EnvBuilder.EnvSessionUUID] = cls._env_id
            if name is None or len(name) == 0:
                cls._name = NameGen.generate_random_name()
            cls._context[EnvBuilder.EnvName] = cls._name

            cls._bootstrap(purge)
        else:
            if name is not None:
                raise RuntimeError("Environment {} is running cannot be renamed or reset".format(cls.__str__()))
        return

    @classmethod
    def get_context(cls) -> Dict:
        return cls._context

    @classmethod
    def _bootstrap(cls,
                   purge: bool) -> None:
        """
        Execute the environment builders.
        Note: At the moment this is hard coded but will move to a YAML settings file.
        :param purge: If true eliminate any existing context and data
        """
        TraceEnvBuilder(cls._context).execute(purge)
        cls._trace = cls.get_trace()
        cls._trace.log().info("Starting {}".format(cls.__str__()))

        RunSpecEnvBuilder(cls._context).execute(purge)
        ElasticEnvBuilder(cls._context).execute(purge)
        TraceElasticEnvBuilder(cls._context).execute(purge)
        KPSEnvBuilder(cls._context).execute(purge)

        cls._trace.log().info("Started {}".format(cls.__str__()))
        return

    @classmethod
    def get_trace(cls) -> Trace:
        if EnvBuilder.TraceContext not in cls.get_context():
            raise ValueError("Ebv context does not (yet) contain a Trace Context")
        # noinspection PyTypeChecker
        return cls._context[EnvBuilder.TraceContext]

    @classmethod
    def get_kps(cls) -> KPubSub:
        if EnvBuilder.KafkaPubSubContext not in cls.get_context():
            raise ValueError("Ebv context does not (yet) contain a Kafka Pub Sub Context")
        # noinspection PyTypeChecker
        return cls._context[EnvBuilder.KafkaPubSubContext]

    @classmethod
    def __str__(cls):
        return "Env: {} - Id: {}".format(cls._name, cls._env_id)

    @classmethod
    def __repr__(cls):
        return cls.__str__()
