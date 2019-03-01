"""Tests the database list class."""

import requests_mock

from acapi.resources.database import Database
from acapi.resources.databaselist import DatabaseList
from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestDatabaseList(BaseTest):
    """Tests the Acquia Cloud API db list class."""

    def test_create(self, mocker):
        " " " Test create call. " " "

        json = [
            {
                "db_cluster": "4",
                "host": "srv-4",
                "instance_name": "mysitedev",
                "name": "mysite",
                "password": "UeytUwwZxpfqutH",
                "username": "mysitedev",
            }
        ]

        # Register the list.
        url = "https://cloudapi.acquia.com/v1/" "sites/prod:mysite/envs/dev/dbs.json"

        mocker.register_uri("GET", url, json=json)

        # Register the create
        mocker.register_uri(
            "POST",
            "https://cloudapi.acquia.com/v1/sites/prod:mysite/dbs.json",
            json=self.generate_task_dictionary(2346, "waiting", False),
        )

        # Register the task.
        mocker.register_uri(
            "GET",
            "https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/2346.json",
            json=self.generate_task_dictionary(2346, "done", True),
        )

        db = self.client.site("mysite").environment("dev").dbs().create("newdb")
        self.assertIsInstance(db, Database)

    def test_get(self, mocker):
        """Test get call."""
        json = [
            {
                "db_cluster": "4",
                "host": "srv-4",
                "instance_name": "mysitedev",
                "name": "mysite",
                "password": "UeytUwwZxpfqutH",
                "username": "mysitedev",
            }
        ]

        url = "https://cloudapi.acquia.com/v1/" "sites/prod:mysite/envs/dev/dbs.json"

        mocker.register_uri("GET", url, json=json)

        dblist = self.client.site("mysite").environment("dev").dbs()
        self.assertIsInstance(dblist, DatabaseList)
