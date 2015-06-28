""" Acquia Cloud API Environment resource. """

import re
from .acquiaresource import AcquiaResource
from .database import Database
from .databaselist import DatabaseList
from .domain import Domain
from .domainlist import DomainList
from .server import Server
from .serverlist import ServerList

class Environment(AcquiaResource):

    """Environment associated with a site."""

    #: Valid keys for environment object.
    valid_keys = ['name', 'vcs_path', 'ssh_host', 'db_clusters', 'default_domain', 'livedev']

    def copy_files(self, target):
        """Copy files to another environment.

        Parameters
        ----------
        target : str
            The name of the environment to copy the files to.

        Returns
        -------
        bool
            Were the files successfully copied?
        """
        pattern = re.compile('/envs/(.*)')
        base_uri = pattern.sub(r'/files-copy/\g<1>', self.uri)
        uri = '{uri}/{target}'.format(uri=base_uri, target=target)

        task_data = self.request(uri=uri, method='POST')
        task = self.create_task(uri, task_data)
        task.wait()

        return True

    def db(self, name):
        """Fetch a database associated with the environment.

        Parameters
        ----------
        name : str
            The name of the database to retrieve.

        Returns
        -------
        Database
            The requested database resource object.
        """
        uri = ('%s/dbs/%s' % (self.uri, name))
        return Database(uri, self.auth)

    def dbs(self):
        """Fetch all databases associated with the environment.

        Returns
        -------
        DatabaseList
            Dictionary of the databases keyed by name.
        """
        dbs = DatabaseList(self.uri, self.auth)
        return dbs

    def deploy_code(self, path):
        """Deploy code to the environment.

        Parameters
        ----------
        path : string
            The git reference path (branch/tag name) to deploy.

        Returns
        -------
        bool
            Was the code successfully deployed?
        """
        uri = '{}/code-deploy'.format(self.uri)
        params = {'path': path}

        task_data = self.request(uri=uri, method='POST', params=params)
        task = self.create_task(uri, task_data)
        task.wait()

        return True

    def domain(self, name):
        """Fetch a domain resource object.

        Parameters
        ----------
        name : string
            The FQDN of the domain to lookup.

        Returns
        -------
        Domain
            The domain resource object.
        """
        uri = '{uri}/domains/{name}'.format(uri=self.uri, name=name)
        return Domain(uri, self.auth)

    def domains(self):
        """Fetch a list of domains associated with the environment.

        returns dict of domains keyed by FQDN.

        """
        domains = DomainList(self.uri, self.auth)
        return domains

    def livedev(self, enable, discard=True):
        """Enable or disable live dev for the domain.

        Parameters
        ----------
        enable : bool
             Enable live development for this environment?
        discard : bool
             Discard all non committed changes?

        Returns
        -------
        Environment
            This environment object.
        """
        action = 'enable'
        params = {}

        if not enable:
            action = 'disable'
        uri = '{uri}/livedev/{action}'.format(uri=self.uri, action=action)

        if discard:
            params['discard'] = 1

        task_data = self.request(uri=uri, method='POST', params=params)
        task = self.create_task(uri, task_data)
        task.wait()

        return self


    def server(self, hostname):
        """Fetch a server associated with the environment.

        name The hostname of the server to lookup.

        return Server object

        """
        uri = ('%s/servers/%s', (self.uri, hostname))
        return Server(uri, self.auth)

    def servers(self):
        """Fetch a list of servers associated with the environment.

        returns dict of servers keyed by hostname.

        """
        servers = ServerList(self.uri, self.auth)
        return servers
