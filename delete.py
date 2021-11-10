import sys

from .utils import run_shell_command, generate_heroku_app_name


def delete(deployment_name, heroku_config):
    app_name = generate_heroku_app_name(deployment_name)
    print(f"Removing app {app_name}")
    run_shell_command(["heroku", "apps:destroy", app_name, "--confirm", app_name])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise Exception("Please provide deployment_name")
    deployment_name = sys.argv[1]

    delete(deployment_name)
