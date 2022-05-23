import os
from typing import List

from bentoctl.exceptions import BentoctlException
from bentoctl.utils.operator_helpers import run_shell_command

HEROKU_REGISTRY = "registry.heroku.com/{deployment_name}/web"
HEROKU_EMAIL_ENV_VAR = "HEROKU_EMAIL"
HEROKU_API_TOKEN_VAR = "HEROKU_API_KEY"


def heroku_run(commands: List[str]):
    try:
        run_shell_command(["heroku", *commands])
    except FileNotFoundError as e:
        if e.filename == "heroku":
            raise BentoctlException(
                "heroku-cli not found! Please make sure that it is installed and available in the current path. For more instructions reffer https://devcenter.heroku.com/articles/heroku-cli"
            )
        else:
            raise


def create_heroku_app(deployment_name: str):
    try:
        heroku_run(["apps:create", "--no-remote", "--json", deployment_name])
    except Exception as e:
        exception_message = e.args[0]
        if f"Name {deployment_name} is already taken" in exception_message:
            raise BentoctlException(
                f"The name {deployment_name} is already taken. Please use a different deployment name."
            )
        else:
            raise


def get_environ_var(var_name: str):
    var_value = os.environ.get(var_name)
    if var_value is None:
        raise BentoctlException(
            f"'{var_name}' not set! Please check the docs on how to generate and set the API key"
        )

    return var_value


def create_repository(deployment_name, operator_spec):
    # try and create app
    create_heroku_app(deployment_name)

    return (
        HEROKU_REGISTRY.format(deployment_name=deployment_name),
        get_environ_var(HEROKU_EMAIL_ENV_VAR),
        get_environ_var(HEROKU_API_TOKEN_VAR),
    )


def delete_repository(deployment_name, operator_spec):
    pass
