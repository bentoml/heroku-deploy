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