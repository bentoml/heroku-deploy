from bentoml.bentos import containerize

from .utils import (
    generate_heroku_resource_names,
    get_tag_from_path,
    push_image,
    run_shell_command,
)


def deploy(bento_path, deployment_name, deployment_spec):
    app_name, repository_url = generate_heroku_resource_names(deployment_name)

    print(f"Create Heroku app {app_name}")
    run_shell_command(["heroku", "apps:create", app_name, "--no-remote"])

    deploy_bento(bento_path, deployment_spec, app_name, repository_url)


def deploy_bento(bento_path, deployment_spec, app_name, repository_url):
    bento_tag = get_tag_from_path(bento_path)
    print("Login Heroku registry")
    run_shell_command(["heroku", "container:login"])

    print("Containerizing the bento")
    containerize(bento_tag.name, docker_image_tag=repository_url)

    print(f"Push Heroku app {app_name}")
    push_image(repository=repository_url)

    print(f"Deploy Heroku app {app_name}")
    run_shell_command(["heroku", "container:release", "web", "--app", app_name])
    run_shell_command(
        [
            "heroku",
            "ps:scale",
            f'worker={deployment_spec["dyno_type"]}:{deployment_spec["dyno_counts"]}',
            "--app",
            app_name,
        ]
    )
