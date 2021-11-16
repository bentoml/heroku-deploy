from .utils import generate_heroku_app_name, run_shell_command


def delete(deployment_name, heroku_config=None):
    app_name = generate_heroku_app_name(deployment_name)
    print(f"Removing app {app_name}")
    run_shell_command(["heroku", "apps:destroy", app_name, "--confirm", app_name])
