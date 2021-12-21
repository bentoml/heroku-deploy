from .utils import generate_heroku_resource_names, run_shell_command


def delete(deployment_name, deployment_spec=None):
    app_name, _ = generate_heroku_resource_names(deployment_name)
    print(f"Removing app {app_name}")
    run_shell_command(["heroku", "apps:destroy", app_name, "--confirm", app_name])
