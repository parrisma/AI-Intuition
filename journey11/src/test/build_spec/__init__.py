import os
#
# Which Git branch are we testing against.
#
from journey11.src.test.build_spec.buildspec import BuildSpec

build_spec_path = os.getenv(BuildSpec.BUILD_SPEC_PATH_ENV_VAR, None)
if build_spec_path is None:
    raise ValueError("Environment variable {} must be defined & point at directory where specs {} can be found".format(
        BuildSpec.BUILD_SPEC_PATH_ENV_VAR, BuildSpec.SPECS_FILE))
if not os.path.isdir(build_spec_path):
    raise ValueError("{} is not a valid directory please update the environment variable {}".format(
        build_spec_path,
        BuildSpec.BUILD_SPEC_PATH_ENV_VAR))
specs_file = "{}/{}".format(build_spec_path, BuildSpec.SPECS_FILE)
if not os.path.exists(specs_file):
    raise ValueError("{} spec file does not exist, please update the environment variable {}".format(
        specs_file,
        BuildSpec.BUILD_SPEC_PATH_ENV_VAR))
BuildSpec(specs_file)

build_spec_to_use = os.getenv(BuildSpec.SPEC_TO_USE_ENV_VAR, None)
if build_spec_to_use is not None:
    BuildSpec.set_spec(build_spec_to_use)
