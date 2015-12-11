""" Tests the domain list class. """
import requests_mock

from . import BaseTest
from ..resources import Domain, DomainList

@requests_mock.Mocker()
class TestDomainList(BaseTest):
    """Tests the Acquia Cloud API domain list class."""

    def test_create(self, mocker):
        """ Test create call. """

        # Register the list.
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
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/prod/domains.json',
            json=json
        )

        # Register the create
        mocker.register_uri(
            'POST',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/prod/domains/foo.com.json',
            json=self.generate_task_dictionary(123, 'waiting', False),
        )

        # Register the task.
        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/tasks/123.json',
            json=self.generate_task_dictionary(123, 'done', True),
        )

        domain = self.client.site('mysite').environment('prod').domains().create('foo.com')
        self.assertIsInstance(domain, Domain)        

    def test_get(self, mocker):
        """ Test get call. """
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
            'https://cloudapi.acquia.com/v1/sites/prod:mysite/envs/prod/domains.json',
            json=json
        )
        
        domainlist = self.client.site('mysite').environment('prod').domains()
        self.assertIsInstance(domainlist, DomainList)
