""" Acquia Cloud API site resource. """

from .acquiaresource import AcquiaResource
from .environment import Environment
from .environmentlist import EnvironmentList
from .task import Task
from .tasklist import TaskList


class Site(AcquiaResource):

    """Site (or subscription) resource."""

    def copy_code(self, source, target):
        """ Copy code from one environment to another.

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

        response = self.request(uri=uri, method='POST')
        task_data = response.content

        task = Task(self.uri, self.auth, data=task_data).wait()
        if None == task['completed']:
            raise Exception('Unable to deploy changes.')

        return True

    def environment(self, name):
        """ Retrieve an environment resource.

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
        """ Retrieve a list of environments.

        Returns
        -------
        EnvironmentList
            Dictionary of environments keyed by name.
        """
        envs = EnvironmentList(self.uri, self.auth)
        response = self.request(uri=envs.uri)
        for env in response.content:
            name = env['name'].encode('ascii', 'ignore')
            env_uri = envs.get_resource_uri(name)
            envs[name] = Environment(env_uri, self.auth, data=env)

        return envs

    def task(self, id):
        """ Retrieve a task.

        Parameters
        ----------
        id : int
            The task identifier.

        Returns
        -------
        Task
            The task resource object.
        """
        uri = ('%s/tasks/%d' % (self.uri, id))
        return Task(uri, self.auth, hack_uri=False)

    def tasks(self):
        """ Retrieve all tasks for the site.

        Returns
        -------
        TaskList
            Dictionary of task resources keyed by id.
        """
        tasks = TaskList(self.uri, self.auth)
        response = self.request(tasks.uri)
        for task in response.content:
            id = int(task['id'])
            task_uri = tasks.get_resource_uri(id)
            tasks[id] = Task(task_uri, self.auth, data=task, hack_uri=False)

        return tasks
