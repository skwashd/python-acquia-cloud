"""Tests the database class."""

import requests_mock

from acapi.resources.backuplist import BackupList
from acapi.resources.database import Database
from acapi.resources import Task
from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestDatabase(BaseTest):
    """Tests the Acquia Cloud API db class."""

    def test_backups(self, mocker):
        """Test create call."""

        json = [
            {
                "checksum": "042f31bebd595b6f2c84b3532d4f1a3b",
                "completed": "1331110381",
                "deleted": "0",
                "id": "22",
                "name": "mysite",
                "path": "backups/dev-mysite-mysitedev-2012-03-07.sql.gz",
                "started": "1331110381",
                "type": "daily",
                "link": "http://mysite.devcloud.acquia-sites.com/AH_DOWNLOAD?t=1342468716&prod=7386761671e68e517a74b7b790ef74d8a8fba7336dbc891cfef133bd29a7b238&d=/mnt/files/mysite.prod/backups/prod-mysite-mysite-2012-07-15.sql.gz",  # noqa: E501
            },
        ]

        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/dev/dbs/mysite/backups.json'

        mocker.register_uri(
            'GET',
            url,
            json=json
        )

        backups = self.client.site('mysite').environment('dev').db(
            'mysite').backups()
        self.assertIsInstance(backups, BackupList)

    def test_copy(self, mocker):
        """Test database copy call."""

        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/dbs/mysite/db-copy/dev/staging.json'

        mocker.register_uri(
            'POST',
            url,
            json=self.generate_task_dictionary(1210, 'waiting', False),
        )

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1210.json',
            json=self.generate_task_dictionary(1210, 'done', True),
        )

        db = self.client.site('mysite').environment('dev').db('mysite').copy(
            'staging')
        self.assertIsInstance(db, Database)

    def test_copy_wait_false(self, mocker):
        """Test database copy call with wait=False."""

        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/dbs/mysite/db-copy/dev/staging.json'

        mocker.register_uri(
            'POST',
            url,
            json=self.generate_task_dictionary(1210, 'waiting', False),
        )

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1210.json',
            json=self.generate_task_dictionary(1210, 'done', True),
        )

        task = self.client.site('mysite').environment('dev').db('mysite').copy(
            'staging', wait=False)
        self.assertIsInstance(task, Task)
