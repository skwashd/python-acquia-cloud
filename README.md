# Python Library for Acquia's Cloud API

This is a python client for using the [Acquia Cloud API](https://cloudapi.acquia.com/).

[![PyPI Version](https://img.shields.io/pypi/v/acapi.svg)](https://pypi.org/project/acapi/)
[![Requirements Status](https://requires.io/github/skwashd/python-acquia-cloud/requirements.svg?branch=master)](https://requires.io/github/skwashd/python-acquia-cloud/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/skwashd/python-acquia-cloud/badge.svg?branch=master&service=github)](https://coveralls.io/github/skwashd/python-acquia-cloud?branch=master)
[![Build Status](https://travis-ci.org/skwashd/python-acquia-cloud.png)](https://travis-ci.org/skwashd/python-acquia-cloud)

## Installation

### Installing With pip (recommended)
`pip install acapi`

## Manual Installation
```
$ git clone git@github.com:skwashd/python-acquia-cloud.git acapi
$ cd acapi
$ ./setup.py build && ./setup.py install
```
## Examples

```python

import acapi

from pprint import pprint

# Acquia subscription name.
subname = 'example'
# Website domain.
domain = 'example.com'

# Instantiate client using environment variables.
# Set ACQUIA_CLOUD_API_USER and ACQUIA_CLOUD_API_TOKEN accordingly.
c = acapi.Client()

# Get the site object.
site = c.site(subname)

# Get the environments object.
envs = site.environments()

# Print all environments on a subscription.
pprint(envs)

# List the SSH host for each environment.
for env in envs:
    print "Env: {env} SSH Host: {host}".format(env=env, host=envs[env]['ssh_host'])

# Move a domain from stage to production.
envs['prod'].domain(domain).move('test')

# Backup the development environment database and download the dump file.
site.environment('dev').db(subname).backups().create().download('/tmp/backup.sql.gz')

```

This library was created and maintained by [Dave Hall](http://davehall.com.au).

See [LICENSE](LICENSE).

[1]: https://requires.io/github/skwashd/python-acquia-cloud/requirements/
[2]: https://requires.io/github/skwashd/python-acquia-cloud/requirements.svg?style=flat
