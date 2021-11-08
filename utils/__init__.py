import re
import json
import subprocess
import cerberus


def run_shell_command(command, cwd=None, env=None, shell_mode=False):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=shell_mode,
        cwd=cwd,
        env=env,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        try:
            return json.loads(stdout.decode("utf-8")), stderr.decode("utf-8")
        except json.JSONDecodeError:
            return stdout.decode("utf-8"), stderr.decode("utf-8")
    else:
        raise Exception(
            f'Failed to run command {" ".join(command)}: {stderr.decode("utf-8")}'
        )


def get_configuration_value(config_file):
    with open(config_file, "r") as file:
        configuration = json.loads(file.read())
    validate_configuration_value(configuration)
    return configuration


def generate_heroku_app_name(deployment_name):
    # Name must start with a letter, end with a letter or digit and can only
    # contain lowercase letters, digits, and dashes. Name is too long
    # (maximum is 30 characters)
    app_name = f"btml-{deployment_name}"[:30]
    invalid_chars = re.compile("[^a-zA-Z0-9-]")
    app_name = re.sub(invalid_chars, "-", app_name)
    return app_name.lower()


def validate_configuration_value(configuration):
    schema = {
    "dyno_counts": {
        "type": "integer",
        "required": True,
        "min": 1
    },
    "dyno_type": {
        "type": "string",
        "allowed": [
            "free",
            "hobby",
            "standard-1x",
            "standard-2x",
            "performance-m",
            "performance-l"
        ],
        "required": True
        },
    }

    v = cerberus.Validator(schema)
    if v.validate(configuration, schema):
        pass
    else:
        raise Exception(
            f"Config validation failed {v.errors}"
        )
