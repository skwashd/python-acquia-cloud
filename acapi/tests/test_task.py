"""Tests the Acquia Cloud API Task class."""
import requests_mock
import sys

from datetime import timedelta

from acapi import exceptions
from acapi.tests import BaseTest

if sys.version_info[0] < 3:
    import mock
else:
    from unittest import mock


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

        with self.assertRaises(exceptions.AcquiaCloudTaskFailedException):
            self.client.site(site).task(tid).wait()

    @mock.patch("acapi.resources.task.timedelta", return_value=timedelta(-1))
    def test_timeout(self, mocker, mock_timedelta):
        """Tests task timeout exceeded."""

        tid = 289466
        site = 'mysite'

        exception_response = self.generate_task_dictionary(tid,
                                                           state='started',
                                                           completed=None)

        responses = [
            {'json': exception_response},
        ]
        url = 'https://cloudapi.acquia.com/v1/' \
              'sites/prod:{site}/tasks/{tid}.json'.format(tid=tid, site=site)

        mocker.register_uri(
            'GET',
            url,
            responses
        )

        with self.assertRaises(exceptions.AcquiaCloudTimeoutError):
            self.client.site(site).task(tid).wait(0)

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
