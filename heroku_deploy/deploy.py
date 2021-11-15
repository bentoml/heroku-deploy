import sys
import argparse
import os

from .utils import run_shell_command, get_configuration_value, generate_heroku_app_name


def deploy(bento_bundle_path, deployment_name, heroku_config):
    app_name = generate_heroku_app_name(deployment_name)

    print("Login Heroku registry")
    run_shell_command(["heroku", "container:login"])

    print(f"Create Heroku app {app_name}")
    run_shell_command(["heroku", "apps:create", app_name, "--no-remote"])

    print(f"Build Heroku app {app_name}")
    run_shell_command(
        ["heroku", "container:push", "web", "--app", app_name], cwd=bento_bundle_path
    )
    print(f"Deploy Heroku app {app_name}")
    run_shell_command(["heroku", "container:release", "web", "--app", app_name])
    run_shell_command(
        [
            "heroku",
            "ps:scale",
            f'worker={heroku_config["dyno_type"]}:{heroku_config["dyno_counts"]}',
            "--app",
            app_name,
        ]
    )
    stdout, stderr = run_shell_command(['heroku', 'apps:info', '--app', app_name])
    print(stdout)

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Deploy the bentoml bundle to Heroku",
        epilog="Check out https://github.com/bentoml/heroku-deploy to know more",
    )
    parser.add_argument(
        "bento_bundle_path", help="Path to bentoml bundle"
    )
    parser.add_argument(
        "deployment_name", help="The name you want to use for your deployment"
    )
    parser.add_argument(
        "config_json",
        help="(optional) The config file for your deployment",
        default=os.path.join(os.getcwd(), "heroku_config.json"),
        nargs="?",
    )
    args = parser.parse_args()

    heroku_config = get_configuration_value(args.config_json)
    deploy(args.bento_bundle_path, args.deployment_name, heroku_config)
    print("Deployment Complete!")
