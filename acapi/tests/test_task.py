""" Tests the Acquia Cloud API Task class. """
import logging
import requests_mock


from . import BaseTest
from .. import Client
from ..resources import Task

@requests_mock.Mocker()
class TestTask(BaseTest):
    """Tests the Acquia Cloud API Task class."""

    def test_task(self, mocker):
        """ Tests fetching a task object. """

        tid = 289466
        site = 'mysite'
        json = self.generate_task_dictionary(tid, state='error')

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:{site}/tasks/{tid}.json'.format(tid=tid, site=site),
            json=json
        )

        task = self.client.site(site).task(tid)
        self.assertEqual(task['id'], tid)
        self.assertEqual(task['state'], 'error')

    def test_wait(self, mocker):
        """ Tests waiting for a task to complete. """

        tid = 289466
        site = 'mysite'
        responses = [
            {'json': self.generate_task_dictionary(tid, state='waiting', completed=False)},
            {'json': self.generate_task_dictionary(tid)},
        ]

        mocker.register_uri(
            'GET',
            'https://cloudapi.acquia.com/v1/sites/prod:{site}/tasks/{tid}.json'.format(tid=tid, site=site),
            responses
        )

        #self.assertTrue(False)
        task = self.client.site(site).task(tid).wait()
        self.assertEqual(task['id'], tid)
        self.assertEqual(task['state'], 'done')
