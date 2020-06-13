#
# Settings specific to a build/test context
#
from typing import List
from journey11.src.lib.transformer import Transformer


# todo: bootstrap from a YML file.


class BuildSpec:
    DEFAULT = "default"

    _specs = dict()

    def __init__(self,
                 git_root: str,
                 branch: str):
        self._git_root = git_root
        self._branch = branch

    def branch(self) -> str:
        return self._branch

    def pubsub_settings_yaml(self) -> str:
        return "{}/{}//journey11/src/test/kpubsubai/settings.yaml".format(self._git_root, self._branch)

    @classmethod
    def get_spec(cls,
                 spec_name: str = None) -> 'BuildSpec':
        if spec_name is None:
            spec_name = BuildSpec.DEFAULT
        return BuildSpec._specs[spec_name]

    @classmethod
    def set_spec(cls,
                 spec_name: str,
                 spec: 'BuildSpec') -> None:
        cls._specs[spec_name] = spec
        return

    def _replace_git_branch(self,
                            s: str) -> str:
        return s.replace('<git-branch>', self._branch, 1)

    def setting_transformers(self) -> List[Transformer.Transform]:
        return [Transformer.Transform(regular_expression='.*<git-branch>.*',
                                      transform=self._replace_git_branch)]
