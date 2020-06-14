from journey11.src.lib.namegen.verbs import Verbs
from journey11.src.lib.namegen.names import Names


class NameGen:
    @staticmethod
    def generate_random_name() -> str:
        return "{}-{}".format(Verbs.random_verb(), Names.random_name())
