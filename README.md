#BentoML Heroku deployment tool


## Prerequisites

- An active Heroku account configured on the machine with AWS CLI installed and configured
    - Install instruction: https://devcenter.heroku.com/articles/heroku-cli#getting-started
    - Login Heroku CLI: `$heroku login`
- Docker is installed and running on the machine.
    - Install instruction: https://docs.docker.com/install
- Install required python packages
    - `$ pip install -r requirements.txt`
    

## Deployment operations

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
