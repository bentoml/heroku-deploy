import json
import re
import subprocess

import fs
import docker
from bentoml.bentos import Bento

PROCESS_NAME = "web"


def run_shell_command(command, cwd=None, env=None, shell_mode=False):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=shell_mode,
        cwd=cwd,
        env=env,
    )
    stdout, stderr = proc.communicate()
    if proc.returncode == 0:
        try:
            return json.loads(stdout.decode("utf-8")), stderr.decode("utf-8")
        except json.JSONDecodeError:
            return stdout.decode("utf-8"), stderr.decode("utf-8")
    else:
        raise Exception(
            f'Failed to run command {" ".join(command)}: {stderr.decode("utf-8")}'
        )


def get_configuration_value(config_file):
    with open(config_file, "r") as file:
        configuration = json.loads(file.read())
    return configuration


def generate_heroku_resource_names(deployment_name):
    # Name must start with a letter, end with a letter or digit and can only
    # contain lowercase letters, digits, and dashes. Name is too long
    # (maximum is 30 characters)
    app_name = f"{deployment_name[:25]}-app"
    invalid_chars = re.compile("[^a-zA-Z0-9-]")
    app_name = re.sub(invalid_chars, "-", app_name).lower()

    repository_url = f"registry.heroku.com/{app_name}/{PROCESS_NAME}"
    return app_name, repository_url


def push_image(
    repository, image_tag=None, username=None, password=None
):
    docker_client = docker.from_env()
    docker_push_kwags = {"repository": repository, "tag": image_tag}
    if username is not None and password is not None:
        docker_push_kwags["auth_config"] = {"username": username, "password": password}
    try:
        docker_client.images.push(**docker_push_kwags)
    except docker.errors.APIError as error:
        raise Exception(f"Failed to push docker image: {error}")


def get_tag_from_path(path: str):
    bento = Bento.from_fs(fs.open_fs(path))
    return bento.tag
