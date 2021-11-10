import sys

from .utils import generate_heroku_app_name, run_shell_command


def describe(deployment_name, heroku_config):
    app_name = generate_heroku_app_name(deployment_name)
    stdout, stderr = run_shell_command(['heroku', 'apps:info', '--app', app_name])
    print(stdout)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Please provide deployment_name")
    deployment_name = sys.argv[1]

    describe(deployment_name)
