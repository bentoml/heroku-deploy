<div align="center">
    <h1>Heroku Operator</h1>
    <p>
        <img src="https://img.shields.io/badge/Release-Alpha-<COLOR>.svg"/>
    </p>
</div>

Heroku is a popular platform as a service(PaaS) based on managed container system. It provides
a complete solution for building, running, and scaling applications

This tool can be used as an Operator for the [bentoctl](https://github.com/bentoml/bentoctl). See steps on how to add Heroku Deployment Tool as an Operator [here](#deploy-to-heroku-with-bentoctl)

<!--ts-->

## Table of Contents

   * [Prerequisites](#prerequisites)
   * [Deploy to Heroku with bentoctl](#deploy-to-heroku-with-bentoctl)
   * [Deploy to Heroku using scripts](#deploy-to-heroku-using-scripts)
   * [Deployment Command Reference](#deployment-command-reference)
      * [Create a Deployment](#create-a-deployment)
      * [Update a Deployment](#update-a-deployment)
      * [Get a Deployment’s Status and Information](#get-a-deployments-status-and-information)
      * [Delete a Deployment](#delete-a-deployment)
      * [Configuring the Deployment](#configuring-the-deployment)

<!-- Added by: jjmachan, at: Wednesday 22 December 2021 03:04:23 PM IST -->

<!--te-->

## Prerequisites

- An active Heroku account configured on the machine with AWS CLI installed and configured
    - Install instruction: https://devcenter.heroku.com/articles/heroku-cli#getting-started
    - Login Heroku CLI: `$heroku login`
- Docker is installed and running on the machine
    - Install instruction: https://docs.docker.com/install
- Built bento
    - Checkout [BentoML quickstart guide](https://github.com/bentoml/BentoML/blob/master/guides/quick-start/bentoml-quick-start-guide.ipynb) for how to get started

## Deploy to Heroku with bentoctl

1. Install bentoctl
    ```bash
    $ pip install bentoctl
    ```

2. Add Heroku operator
    ```bash
    $ bentoctl operator add
    Choose of the Official Operators
    yatai
    > heroku
    aws-lambda
    aws-sagemaker
    asw-ec2
    azure-functions
    azure-container-instances
    google_compute_engine
    google-cloud-run      
    Added heroku!   
    ```

3. Deploy to Heroku use entoctl deploy command
    ```bash
    # Use the interactive mode
    $ bentoctl deploy 
    #
    # or provide deployment spec yaml. See bentoctl repo for more detail
    $ bentoctl deploy --file deployment_spec.yaml
    
    #example response
    Login Heroku registry
    Create Heroku app btml-test-script
    Build Heroku app btml-test-script
    Deploy Heroku app btml-test-script
    === btml-test-script
    Auto Cert Mgmt: false
    Dynos:          web: 1
    Git URL:        https://git.heroku.com/btml-test-script.git
    Owner:          your-email@email.com
    Region:         us
    Repo Size:      0 B
    Slug Size:      0 B
    Stack:          container
    Web URL:        https://btml-test-script.herokuapp.com/
    ```

4. Get deployment information
    ```bash
    $ bentoctl describe my_deployment_spec.yaml
    ```

5. Make sample request
    ```bash
    $ curl -i \
        --header "Content-Type: application/json" \
        --request POST \
        --data '[[5.1, 3.5, 1.4, 0.2]]' \
        https://btml-test-script.herokuapp.com/predict

    # Output
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Type: application/json
    X-Request-Id: f499b6d0-ad9b-4d79-850a-3dc058bd67b2
    Content-Length: 3
    Date: Mon, 28 Jun 2021 02:50:35 GMT
    Server: Python/3.7 aiohttp/3.7.4.post0
    Via: 1.1 vegur

    [0]%
    ```

6. Delete deployment with bentoctl
    ```bash
    $ bentoctl delete deployment_spec.yaml
    ```


## Deploy to Heroku using scripts

1. Download Heroku deployment and install the required packages
    ```bash
    $ git clone https://github.com/bentoml/heroku-deploy.git
    $ cd heroku-deploy
    $ pip install -r requirements.txt
    ```

2. Create Heroku deployment with deployment

    Run deploy script in the command line:
    ```bash
    $ BENTO_BUNDLE_PATH=$(bentoml get IrisClassifier:latest --print-location -q)
    $ ./deploy $BENTO_BUNDLE_PATH test-script heroku_config.json

    # Output
    Login Heroku registry
    Create Heroku app btml-test-script
    Build Heroku app btml-test-script
    Deploy Heroku app btml-test-script
    === btml-test-script
    Auto Cert Mgmt: false
    Dynos:          web: 1
    Git URL:        https://git.heroku.com/btml-test-script.git
    Owner:          yubz86@gmail.com
    Region:         us
    Repo Size:      0 B
    Slug Size:      0 B
    Stack:          container
    Web URL:        https://btml-test-script.herokuapp.com/
    ```

3. Get deployment information
    ```bash
    $ ./describe test-script

    # Output
    === btml-test-script
    Auto Cert Mgmt: false
    Dynos:          web: 1
    Git URL:        https://git.heroku.com/btml-test-script.git
    Owner:          yubz86@gmail.com
    Region:         us
    Repo Size:      0 B
    Slug Size:      0 B
    Stack:          container
    Web URL:        https://btml-test-script.herokuapp.com/
    ```

4. Make sample request against deployed service
    ```bash
    $ curl -i \
        --header "Content-Type: application/json" \
        --request POST \
        --data '[[5.1, 3.5, 1.4, 0.2]]' \
        https://btml-test-script.herokuapp.com/predict

    # Output
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Type: application/json
    X-Request-Id: f499b6d0-ad9b-4d79-850a-3dc058bd67b2
    Content-Length: 3
    Date: Mon, 28 Jun 2021 02:50:35 GMT
    Server: Python/3.7 aiohttp/3.7.4.post0
    Via: 1.1 vegur

    [0]%
    ```

5. Delete Heroku deployment
    ```bash
    $ ./delete test-script

    # Output
    Removing app btml-test-script
    ```

## Deployment Command Reference

### Create a Deployment

Use command line
```bash
$ ./deploy <BENTO_BUNDLE_PATH> <DEPLOYMENT_NAME> <CONFIG_JSON, default is heroku_config.json>
```

Example:
```bash
BENTO_BUNDLE_PATH=${bentoml get IrisClassifier:latest --print-location -q)
$ ./deploy $BENTO_BUNDLE_PATH my_first_deployment heroku_config.json
```

Use Python API
```python
from heroku_deploy import deploy

deploy_heroku(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, HEROKU_CONFIG)
```
* where `HEROKU_CONFIG` is a dictionary with keys for `"dyno_counts"` and `"dyno_type"`

### Update a Deployment

Use command line
```bash
$ ./update <Bento_bundle_path> <Deployment_name> <Config_JSON>
```

Use Python API
```python
from heroku_deploy import update

update(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, HEROKU_CONFIG)
```
* where `HEROKU_CONFIG` is a dictionary with keys for `"dyno_counts"` and `"dyno_type"`

### Get a Deployment’s Status and Information

Use command line
```bash
$ ./describe <DEPLOYMENT_NAME>
```

Use Python API
```python
from heroku_deploy import describe

describe(DEPLOYMENT_NAME)
```

### Delete a Deployment

Use command line
```bash
$ ./delete <Deployment_name>
```

Use Python API
```python
from heroku_deploy import delete

delete(DEPLOYMENT_NAME)
```

### Configuring the Deployment
There is an optional config file available that you can use to specify the configs for your deployment, [heroku_config.json](heroku_config.json). This is the list of configurations you can use to deploy your bento to Heroku. Please refer to the documenation attached to each point for more information about the options
- `dyno_counts`: Number of dynos running for the deployment. A dyno is an isolated, virtualized Linux container that is designed to execute your code. Check the [docs](https://devcenter.heroku.com/articles/dyno-types#default-scaling-limits), and [article](https://www.heroku.com/dynos) for more information
- `dyno_type`: Dyno (instance) type. Each dyno type provides a certain number of RAM, CPU share, Compute, and wheter it sleeps. Check the [docs](https://devcenter.heroku.com/articles/dyno-types) for more information
