from .deploy import deploy_bento
from .utils import generate_heroku_resource_names


def update(bento_path, deployment_name, deployment_spec):
    app_name, repository_url = generate_heroku_resource_names(deployment_name)

    deploy_bento(bento_path, deployment_spec, app_name, repository_url)
