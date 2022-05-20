import os

from bentoctl.exceptions import BentoctlException

USERNAME = "_"
HEROKU_REGISTRY = "registry.heroku.com/{deployment_name}/web"


def create_repository(deployment_name, operator_spec):
    heroku_api_token = os.environ.get("HEROKU_API_KEY")
    if heroku_api_token is None:
        raise BentoctlException(
            "'HEROKU_API_KEY' not set! Please check the docs on how to generate and set the API key"
        )

    return (
        HEROKU_REGISTRY.format(deployment_name=deployment_name),
        USERNAME,
        heroku_api_token,
    )


def delete_repository(deployment_name, operator_spec):
    pass
