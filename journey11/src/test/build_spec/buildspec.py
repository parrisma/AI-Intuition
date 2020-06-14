#
# Settings specific to a build/test context
#
from typing import List
import subprocess
from journey11.src.lib.transformer import Transformer
from journey11.src.lib.settings import Settings
from journey11.src.lib.filestream import FileStream


# todo: bootstrap from a YML file.


class BuildSpec:
    DEFAULT = "default"
    BUILD_SPEC_PATH_ENV_VAR = "BUILD_SPEC_PATH"
    SPECS_FILE = "specs.yml"
    SPEC_TO_USE_ENV_VAR = "BUILD_SPEC_TO_USE"
    M_BRANCH = "_branch"
    M_CURR_BRANCH = "_current_git_branch"
    _settings = None
    _spec = DEFAULT

    @classmethod
    def __init__(cls,
                 bootstrap_yaml_filename: str):
        cls._git_current_branch()
        cls._settings = Settings(settings_yaml_stream=FileStream(bootstrap_yaml_filename),
                                 bespoke_transforms=[cls.current_branch_transformer()])
        cls._spec = cls.DEFAULT
        return

    @classmethod
    def branch(cls) -> str:
        return getattr(cls._settings, "{}{}".format(cls._spec, cls.M_BRANCH))

    @classmethod
    def current_branch(cls) -> str:
        return getattr(cls, "{}".format(cls.M_CURR_BRANCH))

    @classmethod
    def pubsub_settings_yaml(cls) -> str:
        return "{}/{}/{}".format(getattr(cls._settings, "{}_git_root".format(cls._spec)),
                                 getattr(cls._settings, "{}_branch".format(cls._spec)),
                                 getattr(cls._settings, "{}_kafka_yml".format(cls._spec)))

    @classmethod
    def get_spec(cls) -> str:
        return cls._spec

    @classmethod
    def set_spec(cls,
                 spec: str) -> None:
        if hasattr(cls._settings, spec):
            if callable(getattr(cls._settings, cls._spec)):
                cls._spec = spec
            else:
                raise ValueError("No such test spec {} has been loaded from the yaml config".format(spec))
        else:
            raise ValueError("No such test spec {} has been loaded from the yaml config".format(spec))
        return

    @classmethod
    def _git_current_branch(cls):
        res = subprocess.check_output("git rev-parse --abbrev-ref HEAD").decode('utf-8')
        if res is None or len(res) == 0:
            res = "ERROR cannot establish current git branch"
        else:
            res = cls._chomp(res)
        setattr(cls, cls.M_CURR_BRANCH, res)
        return

    @classmethod
    def branch_transformer(cls) -> Transformer.Transform:
        return Transformer.Transform(regular_expression='.*<git-branch>.*',
                                     transform=lambda s: s.replace('<git-branch>', cls.branch(), 1))

    @classmethod
    def current_branch_transformer(cls) -> Transformer.Transform:
        return Transformer.Transform(regular_expression='.*<current-git-branch>.*',
                                     transform=lambda s: s.replace('<current-git-branch>', cls.current_branch(), 1))

    @classmethod
    def setting_transformers(cls) -> List[Transformer.Transform]:
        return [cls.branch_transformer(),
                cls.current_branch_transformer()]

    @staticmethod
    def _chomp(s: str) -> str:
        """
        Remove all line breaks
        :param s: The string to remove line breaks from
        :return: string without line breaks
        """
        return s.replace("\r", "").replace("\n", "")
