Python Library for Acquia's Cloud API
=====================================

This is a python client for using the `Acquia Cloud
API <https://cloudapi.acquia.com/>`__.

|Requirements Status|

Installation
------------

Installing With pip (recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``pip install acapi``

Manual Installation
-------------------

::

    $ git clone git@github.com:skwashd/python-acquia-cloud.git acapi
    $ cd acapi
    $ ./setup.py build && ./setup.py install

Examples
--------

.. code:: python


    import acapi

    from pprint import pprint

    # Acquia subscription name.
    subname = 'example'
    # Website domain.
    domain = 'example.com'

    # Instantiate client using environment variables.
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

This library was created and maintained by `Dave
Hall <http://davehall.com.au>`__.

See `LICENSE <LICENSE>`__.

.. |Requirements Status| image:: https://requires.io/github/skwashd/python-acquia-cloud/requirements.svg?style=flat
   :target: https://requires.io/github/skwashd/python-acquia-cloud/requirements/
