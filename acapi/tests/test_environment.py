""" Tests the environment class. """
import requests_mock

from . import BaseTest
from ..resources import Database, DatabaseList, DomainList, Environment, Server, ServerList

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


    def test_deploy_code(self, mocker):
        """ Tests deploy code call. """
        # Register the deploy action.
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/code-deploy.json?path=tags%2F2012-03-09',
            json=self.generate_task_dictionary(1171, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1171.json',
            json=self.generate_task_dictionary(1171, 'done', True),
        )

        self.assertTrue(self.env.deploy_code('tags/2012-03-09'))


    def test_domains(self, mocker):
        """ Test domain call. """
        json = [
            {
                "name": "foo.com"
            },
            {
                "name": "bar.com"
            },
            {
                "name": "mysite.devcloud.acquia-sites.com"
            }
        ]

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/domains.json',
            json=json,
        )

        self.assertIsInstance(self.env.domains(), DomainList)


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


    def test_livedev_enable(self, mocker):
        """ Test enabling live dev call. """
        #register enable action
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/livedev/enable.json',
            json=self.generate_task_dictionary(1234, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1234.json',
            json=self.generate_task_dictionary(1234, 'done', True),
        )

        self.assertIsInstance(self.env.livedev(True), Environment)


    def test_livedev_disable(self, mocker):
        """ Test disabling live dev call. """
        #register disable action
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/livedev/disable.json?discard=1',
            json=self.generate_task_dictionary(1235, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1235.json',
            json=self.generate_task_dictionary(1235, 'done', True),
        )

        self.assertIsInstance(self.env.livedev(False), Environment)


    def test_livedev_disable_no_discard(self, mocker):
        """ Test disabling live dev call with no discarding. """
        #register disable action
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/livedev/disable.json',
            json=self.generate_task_dictionary(1235, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1235.json',
            json=self.generate_task_dictionary(1235, 'done', True),
        )

        self.assertIsInstance(self.env.livedev(False, False), Environment)


    def test_server(self, mocker):
        """ Tests server call. """

        self.assertIsInstance(self.env.server('server'), Server)


    def test_servers(self, mocker):
        """ Test servers call. """

        json = [
            {
                "name": "web-1",
                "fqdn": "web-1.domain.tld",
                "services": {"web": {"status": "online", "env_status": "inactive"}},
                "status": "online",
                "ami_type": "c1.medium",
                "ec2_region": "us-east-1",
                "ec2_availability_zone": "us-east-1d",
            },
        ]
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/servers.json',
            json=json
        )

        servers = self.env.servers()
        self.assertIsInstance(servers, ServerList)
        self.assertEquals(servers.last()['name'], 'web-1')
