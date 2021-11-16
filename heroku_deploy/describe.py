from .utils import generate_heroku_app_name, run_shell_command


def describe(deployment_name, heroku_config=None):
    app_name = generate_heroku_app_name(deployment_name)
    stdout, stderr = run_shell_command(["heroku", "apps:info", "--app", app_name])
    print(stdout)
