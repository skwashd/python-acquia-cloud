"""Tests the domain class."""

import requests_mock

from acapi.resources import Domain
from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestDomain(BaseTest):
    """Tests the Acquia Cloud API domain class."""

    domain = None

    def setUp(self):
        super(TestDomain, self).setUp()
        self.domain = self.client.site('mysite').environment('prod').domain(
            'foo.com')

    def test_cache_purge(self, mocker):
        """Test cache purge operation."""
        # Register the delete operation.
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/prod/domains/foo.com/cache.json'

        mocker.register_uri(
            'DELETE',
            url,
            json=self.generate_task_dictionary(1137, 'waiting', False),
        )
        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1137.json',
            json=self.generate_task_dictionary(1137, 'done', True),
        )
        self.assertTrue(self.domain.cache_purge())

    def test_delete(self, mocker):
        """Test domain delete operation."""
        # Register the delete operation.
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/prod/domains/foo.com.json'

        mocker.register_uri(
            'DELETE',
            url,
            json=self.generate_task_dictionary(1137, 'waiting', False),
        )
        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/1137.json',
            json=self.generate_task_dictionary(1137, 'done', True),
        )
        self.assertTrue(self.domain.delete())

    def test_get(self, mocker):
        """Test domain get operation."""
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/envs/prod/domains/foo.com.json'

        mocker.register_uri(
            'GET',
            url,
            json={"name": 'foo.com'},
        )
        self.assertEqual(self.domain.get()['name'], 'foo.com')

    def test_move(self, mocker):
        """Test domain move operation."""
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:mysite/domain-move/prod/staging.json'

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

        domain = self.domain.move('staging')
        self.assertIsInstance(domain, Domain)
