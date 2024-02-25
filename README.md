## ⚠️ BentoCTL project has been deprecated

Plese see the latest BentoML documentation on OCI-container based deployment workflow: https://docs.bentoml.com/

## Heroku Operator

Heroku is a popular platform as a service(PaaS) based on managed container system. It provides
a complete solution for building, running, and scaling applications With the combination of [BentoML](https://github.com/bentoml/BentoML) and [bentoctl](https://github.com/bentoml/bentoctl), you can deploy the models built with your favourite ML frameworks easily and manage the infrastructure via terraform.

> **Note:** This operator is compatible with BentoML version 1.0.0 and above. For older versions, please switch to the branch `pre-v1.0` and follow the instructions in the README.md.


## Table of Contents

   * [Quickstart with bentoctl](#quickstart-with-bentoctl)
   * [Configuration Options](#configuration-options)

## Quickstart with bentoctl

This quickstart will walk you through deploying a bento into Heroku. Make sure to go through the [prerequisites](#prerequisites) section and follow the instructions to set everything up.

### Prerequisites

1. Heroku CLI - Make sure that Heroku CLI is installed and you are logged in with an existing heroku account. [Installation instructions](https://devcenter.heroku.com/articles/heroku-cli)
2. Terraform - Terraform is a tool for building, configuring, and managing infrastructure. Installation instructions: www.terraform.io/downloads
3. Docker - Install instructions: https://docs.docker.com/install
4. A working bento - for this guide, we will use the iris-classifier bento from the BentoML [quickstart guide](https://docs.bentoml.org/en/latest/quickstart.html#quickstart) or [import a prebuilt bento](https://github.com/bentoml/bentoctl/blob/main/docs/quickstart.md#step-1-import-a-bento) from S3


### steps

1. Install bentoctl
    ```bash
    $ pip install bentoctl
    ```

2. Install the operator

    Bentoctl will install the official Heroku operator and its dependencies. The Operator contains the Terraform templates and sets up the registries reqired to deploy to GCP.

    ```bash
    bentoctl operator install heroku
    ```

3. Initialize deployment with bentoctl

    Follow the interactive guide to initialize the deployment project.

    ```bash
    $ bentoctl init
    
    Bentoctl Interactive Deployment Config Builder

    Welcome! You are now in interactive mode.

    This mode will help you set up the deployment_config.yaml file required for
    deployment. Fill out the appropriate values for the fields.

    (deployment config will be saved to: ./deployment_config.yaml)

    api_version: v1
    name: quickstart
    operator: heroku
    template: terraform
    spec:
        dyno_counts: 1
        dyno_type: free
    filename for deployment_config [deployment_config.yaml]:
    deployment config generated to: deployment_config.yaml
    ✨ generated template files.
      - ./main.tf
      - ./bentoctl.tfvars
    ```
    > Note: the `name` attribute for the deployment config will be the same name the name for the heroku app that will be generated. If the a heroku app with the same name exists bentoctl will throw an error at the next step so you might have to change it.
   
    This will also run the `bentoctl generate` command for you and will generate the `main.tf` terraform file, which specifies the resources to be created and the `bentoctl.tfvars` file which contains the values for the variables used in the `main.tf` file.

4. Build and push docker image into Heroku registry.

    ```bash
    bentoctl build -b iris_classifier:latest -f deployment_config.yaml
    ```
    The iris-classifier service is now built and pushed into the container registry and the required terraform files have been created. Now we can use terraform to perform the deployment. The heroku app will also be created in this step an as noted above will throw an error if the app_name already exists. Please change the name in the deploymetn_config.yaml file and run the `bentoctl generate` and `bentoctl build` command again.
    
5. Apply Deployment with Terraform

   1. Initialize terraform project. This installs the providers and sets up the terraform folders.
        ```bash
        terraform init
        ```

   2. Apply terraform project to create heroku deployment

        ```bash
        terraform apply -var-file=bentoctl.tfvars -auto-approve
        ```

6. Test deployed endpoint

    The `iris_classifier` uses the `/classify` endpoint for receiving requests so the full URL for the classifier will be in the form `{EndpointUrl}/classify`.

    ```bash
    URL=$(terraform output -json | jq -r .app_url.value)/classify
    curl -i \
      --header "Content-Type: application/json" \
      --request POST \
      --data '[5.1, 3.5, 1.4, 0.2]' \
      $URL
    ```

7. Delete deployment
    Use the `bentoctl destroy` command to remove the registry and the deployment

    ```bash
    bentoctl destroy -f deployment_config.yaml
    ```
    
## Configuration Options
This is the list of configurations you can use to deploy your bento to Heroku. For more information about options check the corresponding Heroku docs provided.

- `dyno_counts`: Number of dynos running for the deployment. A dyno is an isolated, virtualized Linux container that is designed to execute your code. Check the [docs](https://devcenter.heroku.com/articles/dyno-types#default-scaling-limits), and [article](https://www.heroku.com/dynos) for more information
- `dyno_type`: Dyno (instance) type. Each dyno type provides a certain number of RAM, CPU share, Compute, and wheter it sleeps. Check the [docs](https://devcenter.heroku.com/articles/dyno-types) for more information
