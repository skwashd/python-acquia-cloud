""" Tests the backup list class. """
import json
import requests_mock

from . import BaseTest
from ..resources import Backup, BackupList

@requests_mock.Mocker()
class TestBackupList(BaseTest):
    """Tests the Acquia Cloud API backup list class."""

    def test_create(self, mocker):
        """ Test create call. """

        backups = [
            {
                "checksum": "042f31bebd595b6f2c84b3532d4f1a3b",
                "completed": 1331110381,
                "deleted": 0,
                "id": 22,
                "name": "mysite",
                "path": "backups/dev-mysite-mysitedev-2012-03-07.sql.gz",
                "started": 1331110381,
                "type": "daily",
                "link": "http://mysite.devcloud.acquia-sites.com/AH_DOWNLOAD?t=1342468716&prod=7386761671e68e517a74b7b790ef74d8a8fba7336dbc891cfef133bd29a7b238&d=/mnt/files/mysite.prod/backups/prod-mysite-mysite-2012-07-15.sql.gz"
            },
        ]

        # Register the list.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/dbs/mysite/backups.json',
            json=backups
        )

        # Register the create
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/dev/dbs/mysite/backups.json',
            json=self.generate_task_dictionary(1116, 'waiting', False),
        )

        task=self.generate_task_dictionary(1116, 'done', True)
        # Yo Dawg, I herd you like JSON, so I put a JSON in your JSON so you can JSON while you JSON.
        task['result'] = json.dumps({'backupid': 37})

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1116.json',
            json=task
        )

        backup = self.client.site('mysite').environment('dev').db('mysite').backups().create()
        self.assertIsInstance(backup, Backup)
