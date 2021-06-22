import sys

from utils import get_configuration_value, generate_heroku_app_name, run_shell_command


def update_heroku(bento_bundle_path, deployment_name, config_json):
    heroku_config = get_configuration_value(config_json)

    app_name = generate_heroku_app_name(deployment_name)

    print("Login Heroku registry")
    run_shell_command(["heroku", "container:login"])

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


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise Exception(
            "Please provide bento_bundle_path deployment_name and configuration json"
        )
    bento_bundle_path = sys.argv[1]
    deployment_name = sys.argv[2]
    config_json = sys.argv[3] if sys.argv[3] else "heroku_config.json"

    update_heroku(bento_bundle_path, deployment_name, config_json)
