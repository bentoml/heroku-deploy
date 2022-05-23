import os

from bentoctl.utils.operator_helpers.generate import (
    TERRAFORM_VALUES_FILE_NAME,
    Generate,
)
from bentoctl.utils.operator_helpers.values import DeploymentValues

HEROKU_IMAGE_VERSION = "latest"


class HerokuDeploymentValues(DeploymentValues):
    @staticmethod
    def parse_image_tag(image_tag: str):
        registry_url, app_name, _ = image_tag.split("/")

        return registry_url, app_name, HEROKU_IMAGE_VERSION


class HerokuGenerate(Generate):
    @staticmethod
    def generate_terraform_values(name: str, spec: dict, destination_dir: str):

        params = HerokuDeploymentValues(name, spec, "terraform")

        values_file = os.path.join(destination_dir, TERRAFORM_VALUES_FILE_NAME)
        params.to_params_file(values_file)

        return values_file


generate = HerokuGenerate(os.path.join(os.path.dirname(__file__), "templates"))
