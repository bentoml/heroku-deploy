import sys
import argparse

from .utils import generate_heroku_app_name, run_shell_command


def describe(deployment_name, heroku_config=None):
    app_name = generate_heroku_app_name(deployment_name)
    stdout, stderr = run_shell_command(['heroku', 'apps:info', '--app', app_name])
    print(stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Describe the bentoml bundle deployed to Heroku",
        epilog="Check out https://github.com/bentoml/heroku-deploy to know more",
    )
    parser.add_argument(
        "deployment_name", help="The name you used for your deployment"
    )
    args = parser.parse_args()

    describe(args.deployment_name)
