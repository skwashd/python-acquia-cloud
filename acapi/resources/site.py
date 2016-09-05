"""Acquia Cloud API site resource. """

from acapi.resources.acquiaresource import AcquiaResource
from acapi.resources.environment import Environment
from acapi.resources.environmentlist import EnvironmentList
from acapi.resources.task import Task
from acapi.resources.tasklist import TaskList


class Site(AcquiaResource):
    """Site (or subscription) resource."""

    #: Valid keys for site object.
    valid_keys = ['title', 'name', 'production_mode', 'unix_username',
                  'vcs_type', 'vcs_url']

    def copy_code(self, source, target):
        """Copy code from one environment to another.

        Parameters
        ----------
        source : str
            The name of the source environment.
        target : str
            The name of the target environment.

        Returns
        -------
        bool
            Was the code successfully copied?
        """
        uri = '{base}/code-deploy/{source}/{target}'.format(
            base=self.uri,
            source=source, target=target)

        task_data = self.request(uri=uri, method='POST')
        task = self.create_task(uri, task_data)
        task.wait()

        return True

    def environment(self, name):
        """Retrieve an environment resource.

        Parameters
        ----------
        name : str
            The name of the environment.

        Returns
        -------
        Environment
            The environment resource object.
        """
        uri = '{uri}/envs/{name}'.format(uri=self.uri, name=name)
        return Environment(uri, self.auth)

    def environments(self):
        """Retrieve a list of environments.

        Returns
        -------
        EnvironmentList
            Dictionary of environments keyed by name.
        """
        envs = EnvironmentList(self.uri, self.auth)
        return envs

    def task(self, task_id):
        """Retrieve a task.

        Parameters
        ----------
        task_id : int
            The task identifier.

        Returns
        -------
        Task
            The task resource object.
        """
        uri = ('%s/tasks/%d' % (self.uri, task_id))
        return Task(uri, self.auth, hack_uri=False)

    def tasks(self):
        """Retrieve all tasks for the site.

        Returns
        -------
        TaskList
            Dictionary of task resources keyed by id.
        """
        tasks = TaskList(self.uri, self.auth)
        return tasks
