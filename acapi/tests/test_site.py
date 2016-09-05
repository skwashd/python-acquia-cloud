"""Tests the sites class."""

import requests_mock

from acapi.resources.environment import Environment
from acapi.resources.environmentlist import EnvironmentList
from acapi.resources.task import Task
from acapi.resources.tasklist import TaskList
from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestSite(BaseTest):
    """Tests the Acquia Cloud API sites class."""

    site = None

    def setUp(self):
        super(TestSite, self).setUp()
        self.site = self.client.site('mysite')

    def test_copy_code(self, mocker):
        """Tests copying code from one environment to another. """

        source = 'dev'
        target = 'staging'
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/code-deploy/' \
              '{source}/{target}.json'.format(source=source, target=target)

        # Register the copy action.
        mocker.register_uri(
            'POST',
            url,
            json=self.generate_task_dictionary(1137, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1137.json',
            json=self.generate_task_dictionary(1137, 'done', True),
        )

        self.site.copy_code(source, target)

    def test_environment(self, mocker):
        """Tests environment() method."""

        name = 'dev'

        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/{}.json'.format(name)
        json = {
            "name": name,
            "vcs_path": "master",
            "ssh_host": "srv-1.devcloud.hosting.acquia.com",
            "db_clusters": ["4"],
            "default_domain": "mysited.msmith.ahclouddev.com",
            "livedev": "disabled"
        }
        mocker.register_uri(
            'GET',
            url,
            json=json
        )

        env = self.site.environment('dev')
        self.assertIsInstance(env, Environment)
        self.assertEqual(env['name'], name)

    def test_environments(self, mocker):
        """Tests environments() method."""

        url = 'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs.json'
        json = [
            {
                "name": "prod",
                "vcs_path": "tags/WELCOME",
                "ssh_host": "srv-1.devcloud.hosting.acquia.com",
                "db_clusters": ["4"],
                "default_domain": "mysite.msmith.ahclouddev.com",
                "livedev": "disabled",
            },
            {
                "name": "dev",
                "vcs_path": "master",
                "ssh_host": "srv-1.devcloud.hosting.acquia.com",
                "db_clusters": ["4"],
                "default_domain": "mysite.msmith.ahclouddev.com",
                "livedev": "disabled",
            }
        ]
        mocker.register_uri(
            'GET',
            url,
            json=json
        )

        env = self.site.environments()
        self.assertIsInstance(env, EnvironmentList)
        # TODO(skwashd) move this to test_environments
        self.assertEqual(env.first()['livedev'], 'disabled')
        self.assertEqual(env.last()['default_domain'],
                         'mysite.msmith.ahclouddev.com')
        self.assertEqual(env['prod']['name'], 'prod')

    def test_task(self, mocker):
        """Tests single site task request."""
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/tasks/289466.json'

        json = {
            "completed": None,
            "created": "1331259657",
            "description": "Copy files from dev to prod",
            "id": "1213",
            "logs": "[02:20:58] [02:20:58] Started\n"
                    "[02:21:00] [02:21:00] Failure\n",
            "queue": "files-migrate",
            "result": "",
            "sender": "cloud_api",
            "started": "1331259658",
            "state": "error"
        }

        mocker.register_uri(
            'GET',
            url,
            json=json
        )

        task = self.site.task(289466)
        self.assertIsInstance(task, Task)

    def test_tasks(self, mocker):
        """Tests site task list request."""
        url = 'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks.json'
        json = [
            {
                "completed": "1331254866",
                "created": "1331254863",
                "description": "Backup database mysite in dev environment.",
                "id": "988",
                "logs": "[01:01:04] [01:01:04] Started\n"
                        "[01:01:06] [01:01:06] Done\n",
                "queue": "create-db-backup-ondemand",
                "result": "{\"backupid\":\"37\"}",
                "sender": "cloud_api",
                "started": "1331254864",
                "state": "done"
            },
        ]

        mocker.register_uri(
            'GET',
            url,
            json=json
        )

        tasks = self.site.tasks()
        self.assertIsInstance(tasks, TaskList)
        self.assertEqual(len(tasks), 1)
