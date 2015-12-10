""" Tests the environment class. """
import requests_mock

from . import BaseTest
from ..resources import Database, DatabaseList

@requests_mock.Mocker()
class TestSite(BaseTest):
    """Tests the Acquia Cloud API environment class."""

    env = None

    def setUp(self):
        super(TestSite, self).setUp()
        self.env = self.client.site('mysite').environment('dev')


    def test_copy_files(self, mocker):
        """ Tests copying files from one environment to another. """
        source = 'dev'
        target = 'staging'

        # Register the copy action.
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/files-copy/{source}/{target}.json'.format(source=source, target=target),
            json=self.generate_task_dictionary(1213, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1213.json',
            json=self.generate_task_dictionary(1213, 'done', True),
        )

        self.assertTrue(self.env.copy_files(target))


    def test_db(self, mocker):
        """ Tests db call. """
        db = self.env.db('mysite')
        self.assertIsInstance(db, Database)


    def test_dbs(self, mocker):
        """ Tests dbs call. """
        json = [
            {
                "db_cluster": "4",
                "host": "srv-4",
                "instance_name": "mysitedev",
                "name": "mysite",
                "password": "UeytUwwZxpfqutH",
                "username": "mysitedev"
            }
        ]
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/dbs.json',
            json=json
        )

        dbs = self.env.dbs()
        self.assertIsInstance(dbs, DatabaseList)
        self.assertEquals(dbs.first()['name'], 'mysite')


    def test_get(self, mocker):
        """ Tests get call. """

        json = {
            "name": "dev",
            "vcs_path": "master",
            "ssh_host": "srv-1.devcloud.hosting.acquia.com",
            "db_clusters": ["4"],
            "default_domain": "mysited.msmith.ahclouddev.com",
            "livedev": "disabled"
        }

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev.json',
            json=json,
        )

        env = self.env.get()
        self.assertEquals(env['name'], 'dev')
