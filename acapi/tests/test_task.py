"""Tests the Acquia Cloud API Task class."""

import requests_mock

from acapi.exceptions import AcquiaCloudTaskFailedException
from acapi.tests import BaseTest


@requests_mock.Mocker()
class TestTask(BaseTest):
    """Tests the Acquia Cloud API Task class."""

    def test_task(self, mocker):
        """Tests fetching a task object."""

        tid = 289466
        site = 'mysite'
        json = self.generate_task_dictionary(tid, state='error')
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:{site}/tasks/{tid}.json'.format(tid=tid, site=site)

        mocker.register_uri(
            'GET',
            url,
            json=json
        )

        task = self.client.site(site).task(tid)
        self.assertEqual(task['id'], tid)
        self.assertEqual(task['state'], 'error')

    def test_fail(self, mocker):
        """Tests task failure."""

        tid = 289466
        site = 'mysite'
        first_response = self.generate_task_dictionary(tid,
                                                       state='waiting',
                                                       completed=False)

        exception_response = self.generate_task_dictionary(tid,
                                                           state='failed',
                                                           completed=True)

        responses = [
            {'json': first_response},
            {'json': exception_response},
        ]
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:{site}/tasks/{tid}.json'.format(tid=tid, site=site)

        mocker.register_uri(
            'GET',
            url,
            responses
        )

        with self.assertRaises(AcquiaCloudTaskFailedException):
            self.client.site(site).task(tid).wait()

    def test_wait(self, mocker):
        """Tests waiting for a task to complete."""

        tid = 289466
        site = 'mysite'
        first_response = self.generate_task_dictionary(tid,
                                                       state='waiting',
                                                       completed=False)

        responses = [
            {'json': first_response},
            {'json': self.generate_task_dictionary(tid)},
        ]
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:{site}/tasks/{tid}.json'.format(tid=tid, site=site)

        mocker.register_uri(
            'GET',
            url,
            responses
        )

        task = self.client.site(site).task(tid).wait()
        self.assertEqual(task['id'], tid)
        self.assertEqual(task['state'], 'done')
