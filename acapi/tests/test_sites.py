""" Tests the sites class. """
import requests_mock

from . import BaseTest
from ..resources import Environment, EnvironmentList

@requests_mock.Mocker()
class TestSite(BaseTest):
    """Tests the Acquia Cloud API sites class."""

    site = None

    def setUp(self):
        super(TestSite, self).setUp()
        self.site = self.client.site('mysite')

    def test_environment(self, mocker):
        """ Tests environment() method. """

        name = 'dev'

        url = 'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/{}.json'.format(name)
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
        self.assertEquals(env['name'], name)

    def test_environments(self, mocker):
        """ Tests environments() method. """

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
        self.assertEquals(env.first()['livedev'], 'disabled')
        self.assertEquals(env.last()['default_domain'], 'mysite.msmith.ahclouddev.com')
        self.assertEquals(env['prod']['name'], 'prod')
