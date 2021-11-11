import sys
import argparse

from .utils import run_shell_command, generate_heroku_app_name


def delete(deployment_name, heroku_config=None):
    app_name = generate_heroku_app_name(deployment_name)
    print(f"Removing app {app_name}")
    run_shell_command(["heroku", "apps:destroy", app_name, "--confirm", app_name])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete the bentoml bundle deployed to Heroku",
        epilog="Check out https://github.com/bentoml/heroku-deploy to know more",
    )
    parser.add_argument(
        "deployment_name", help="The name you used for your deployment"
    )
    args = parser.parse_args()

    delete(args.deployment_name)
