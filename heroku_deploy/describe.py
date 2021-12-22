from .utils import generate_heroku_resource_names, run_shell_command


def describe(deployment_name, deployment_spec=None):
    app_name, _ = generate_heroku_resource_names(deployment_name)
    stdout, stderr = run_shell_command(["heroku", "apps:info", "--app", app_name])
    print(stdout)
