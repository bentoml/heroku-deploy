# BentoML Heroku deployment tool

[![Generic badge](https://img.shields.io/badge/Release-Alpha-<COLOR>.svg)](https://shields.io/)

Heroku is a popular platform as a service(PaaS) based on managed container system. It provides
a complete solution for build, run and scale applications.


## Prerequisites

- An active Heroku account configured on the machine with AWS CLI installed and configured
    - Install instruction: https://devcenter.heroku.com/articles/heroku-cli#getting-started
    - Login Heroku CLI: `$heroku login`
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install
- Install required python packages
    - `$ pip install -r requirements.txt`


## Deploy Quickstart Iris classifier to Heroku

1. Build and save Bento Bundle from [BentoML quick start guide](https://github.com/bentoml/BentoML/blob/master/guides/quick-start/bentoml-quick-start-guide.ipynb)

2. Create Heroku deployment with deploy script

    Run deploy script in the command line:
    ```bash
    $ BENTO_BUNDLE_PATH=$(bentoml get IrisClassifier:latest --print-location -q)
    $ python deploy.py $BENTO_BUNDLE_PATH test-script heroku_config.json

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
    $ python describe.py test-script

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
    $ python delete.py test-script

    # Output
    Removing app btml-test-script
    ```

## Deployment command reference

### Create a deployment

Use command line
```commandline
$ python deploy.py <Bento_bundle_path> <Deployment_name> <Config_JSON default is heroku_config.json>
```

Example:
```bash
$ MY_BUNDLE_PATH=${bentoml get IrisClassifier:latest --print-location -q)
$ python deploy.py $MY_BUNDLE_PATH my_first_deployment heroku_config.json
```

Use Python API
```python
from deploy import deploy_heroku

deploy_heroku(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, CONFIG_JSON)
```

#### Available options

* `dyno_counts`: Amount of dyno running for the deployment, see https://devcenter.heroku.com/articles/dyno-types#default-scaling-limits for more information.
* `dyno_type`: Heroku dyno(instance) type, see https://devcenter.heroku.com/articles/dyno-types for more information

### Update a deployment

Use command line
```commandline
$ python update.py <Bento_bundle_path> <Deployment_name> <Config_JSON>
```

Use Python API
```python
from update import update_heroku

update_heroku(BENTO_BUNDLE_PATH, DEPLOYMENT_NAME, CONFIG_JSON)
```

### Get a deployment's status and information

Use command line
```commandline
$ python describe.py <Deployment_name>
```

Use Python API
```python
from describe import describe_heroku

describe_heroku(DEPLOYMENT_NAME)
```

### Delete a deployment

Use command line
```commandline
$ python delete.py <Deployment_name>
```

Use Python API
```python
from delete import delete_heroku

delete_heroku(DEPLOYMENT_NAME)
```
