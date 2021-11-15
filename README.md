# BentoML Heroku Deployment Tool

[![Generic badge](https://img.shields.io/badge/Release-Alpha-<COLOR>.svg)](https://shields.io/)

Heroku is a popular platform as a service(PaaS) based on managed container system. It provides
a complete solution for building, running, and scaling applications.

This tool can be used as an Operator for the [Bento Cloud Deployment Tool](https://github.com/bentoml/cloud-deployment-tool/tree/prototype). See steps on how to add Heroku Deployment Tool as an Operator [here](#operator-deployment). 

## Prerequisites

- An active Heroku account configured on the machine with AWS CLI installed and configured
    - Install instruction: https://devcenter.heroku.com/articles/heroku-cli#getting-started
    - Login Heroku CLI: `$heroku login`
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install
- Install required python packages
    - `$ pip install -r requirements.txt`


## Deploy the quick start guide's IrisClassifier to Heroku

1. Build and save Bento Bundle from [BentoML quick start guide](https://github.com/bentoml/BentoML/blob/master/guides/quick-start/bentoml-quick-start-guide.ipynb)

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

## Deployment command reference

### Create a deployment

Use command line

```bash
$ ./deploy <Bento_bundle_path> <Deployment_name> <Config_JSON, default is heroku_config.json>
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

#### Available options

* `dyno_counts`: Amount of dyno running for the deployment, see https://devcenter.heroku.com/articles/dyno-types#default-scaling-limits for more information.
* `dyno_type`: Heroku dyno(instance) type, see https://devcenter.heroku.com/articles/dyno-types for more information

### Update a deployment

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

### Get a deployment's status and information

Use command line

```bash
$ ./describe <Deployment_name>
```

Use Python API

```python
from heroku_deploy import describe

describe(DEPLOYMENT_NAME)
```

### Delete a deployment

Use command line

```bash
$ ./delete <Deployment_name>
```

Use Python API

```python
from heroku_deploy import delete

delete(DEPLOYMENT_NAME)
```

## Operator Deployment

To add the Heroku Deployment Tool as an operator for the Bento Cloud Deployment Tool:

1. Install `bcdt` from the [repo](https://github.com/bentoml/cloud-deployment-tool/tree/prototype)
```bash
$ git clone git@github.com:bentoml/cloud-deployment-tool.git
$ git checkout prototype
$ pip install --editable .
```
2. Install `heroku-deploy`
```bash
$ git clone git@github.com:bentoml/heroku-deploy.git
```
3. Add `heroku` as an operator for `bcdt`
```bash
$ bcdt operators add heroku-deploy/
$ bcdt operators list
{'heroku': ['/home/damir/Git/heroku-deploy', None]}
```
4. Deploy using the Heroku Deployment Tool as an Operator for `bcdt`
```bash
$ bcdt deploy
Interactive Deployment Spec Builder

Welcome! You are now in interactive mode.

This mode will help you setup the deployment_spec.yaml file required for
deployment. Fill out the appropriate values for the fields.

(deployment spec will be saved to: ./deployment_spec.yaml)

api_version: v1
metadata: 
    name: test-script
    operator: heroku
    bento: $BENTO_BUNDLE_PATH
spec: 
    dyno_counts: 1
    dyno_type: free
deployment spec file exists! Should I overide? [Y/n]: Y
deployment spec generated to: deployment_spec.yaml
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
