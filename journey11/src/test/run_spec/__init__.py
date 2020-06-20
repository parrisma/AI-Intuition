import os
#
# Environment specific settings for platform build/test/run
#
from journey11.src.test.run_spec.runspec import RunSpec

if not RunSpec.is_running():
    run_spec_path = os.getenv(RunSpec.RUN_SPEC_PATH_ENV_VAR, None)
    if run_spec_path is None:
        raise ValueError(
            "Environment variable {} must be defined & point at directory where run specs {} can be found".format(
                RunSpec.RUN_SPEC_PATH_ENV_VAR, RunSpec.SPECS_FILE))
    if not os.path.isdir(run_spec_path):
        raise ValueError("{} is not a valid directory please update the environment variable {}".format(
            run_spec_path,
            RunSpec.RUN_SPEC_PATH_ENV_VAR))
    specs_file = "{}/{}".format(run_spec_path, RunSpec.SPECS_FILE)
    if not os.path.exists(specs_file):
        raise ValueError("{} run spec file does not exist, please update the environment variable {}".format(
            specs_file,
            RunSpec.RUN_SPEC_PATH_ENV_VAR))
    RunSpec(specs_file)

    run_spec_to_use = os.getenv(RunSpec.SPEC_TO_USE_ENV_VAR, None)
    if run_spec_to_use is not None:
        RunSpec.set_spec(run_spec_to_use)
