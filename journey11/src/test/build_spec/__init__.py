#
# Which Git branch are we testing against.
#
from .buildspec import BuildSpec

BuildSpec.set_spec(BuildSpec.DEFAULT,
                   BuildSpec(git_root="https://raw.githubusercontent.com/parrisma/AI-Intuition/",
                             branch='kafka'))
