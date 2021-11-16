from .utils import generate_heroku_app_name, get_configuration_value, run_shell_command


def update(bento_bundle_path, deployment_name, heroku_config):
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
    stdout, stderr = run_shell_command(["heroku", "apps:info", "--app", app_name])
    print(stdout)
